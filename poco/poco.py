# -*- coding: utf-8 -*-
import codecs
import datetime
import os
from functools import wraps

import bottle
from bottle import (
    route,
    run,
    jinja2_template as template,
    redirect,
    request,
    response,
    static_file,
)
from bottle_utils.flash import message_plugin

from middleware.twitter import TwitterMiddleware
import utils
from models import get_or_create_tweet
from search import search_tweets
from twitter import fetch_tweet_data, get_cached_oembed, get_oembed
from pagination import Pagination


bottle.install(message_plugin)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
twitter_config = {
  'consumer_key': os.environ['POCO_CONSUMER_KEY'],
  'consumer_secret': os.environ['POCO_CONSUMER_SECRET'],
  'callback_url': 'http://127.0.0.1:8000/verify',
}
app = TwitterMiddleware(bottle.app(), twitter_config)


def login_required(f):
    @wraps(f)
    def _login_required(*args, **kwargs):
        twitter = request.environ.get('twitter')
        if twitter.api is None:
            return redirect('/')
        return f(*args, **kwargs)
    return _login_required


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=STATIC_DIR)


@route('/')
def index():
    return template('index')


@route('/oauth')
def oauth():
    twitter = request.environ.get('twitter')
    redirect_url = twitter.get_authorization_url()
    return redirect(redirect_url)


@route('/verify')
def verify():
    twitter = request.environ.get('twitter')
    verifier = request.params.get('oauth_verifier')
    twitter.authenticate(verifier)
    return redirect('home')


@route('/home')
@route('/home/<page:int>/')
@login_required
def home(page=1):
    twitter = request.environ.get('twitter')
    user = twitter.api.me()
    render_data_list = []
    paginator = None
    if request.query:
        q = request.query
        search_criteria = {
            'since': datetime.datetime.strptime(q['since'], '%Y-%m-%d') if q['since'] else None,
            'until': datetime.datetime.strptime(q['until'], '%Y-%m-%d') if q['until'] else None,
            'media_only': 'media_only' in q,
            'screen_name': q['screen_name'],
            'user_id': q['user_id']
        }

        tweets = search_tweets(search_criteria, selections=['tweet_id'])

        _data_list = fetch_tweet_data(twitter.api, tweets)
        sorted_data = utils.sort_by(q['sort_by'], _data_list, reverse=True)

        paginator = Pagination(sorted_data, per_page=10, current_page=page)
        paginated_data = paginator.paginate()

        # Set oEmbed
        render_data_list = []
        for data in paginated_data:
            try:
                data['oembed'] = get_cached_oembed(twitter.api, data['tweet_id'])
            except EOFError:
                data['oembed'] = get_oembed(twitter.api, data['tweet_id'])
            render_data_list.append(data)

    return template('home', user=user, data_list=render_data_list, paginator=paginator,
                    query_string=request.query_string, params=request.params)


@route('/import')
@login_required
def import_csv():
    return template('import', message=request.message)


@route('/import', method='POST')
@login_required
def do_import_csv():
    twitter = request.environ.get('twitter')
    file = request.files.get('file')
    name, ext = os.path.splitext(file.filename)
    if ext not in ('.csv', '.txt'):
        response.flash("File extension not allowed.")
        redirect('import')
    user = twitter.api.me()
    user_id = user.id
    for data in utils.parse_tweets_csv(codecs.iterdecode(file.file, 'utf8')):
        data['user_id'] = user_id
        get_or_create_tweet(data)
    return redirect('home')


if __name__ == "__main__":
    from models import create_sqlite_table
    create_sqlite_table()
    run(app=app, host="localhost", port=8000, debug=True, reloader=True)

