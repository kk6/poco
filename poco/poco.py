# -*- coding: utf-8 -*-
import codecs
import datetime
import os

import bottle
from bottle import (
    route,
    run,
    jinja2_template as template,
    redirect,
    request,
)
from middleware.twitter import TwitterMiddleware
import utils
from models import create_or_update_tweet
from search import search_tweets

twitter_config = {
  'consumer_key': os.environ['POCO_CONSUMER_KEY'],
  'consumer_secret': os.environ['POCO_CONSUMER_SECRET'],
  'callback_url': 'http://127.0.0.1:8000/verify',
}
app = TwitterMiddleware(bottle.app(), twitter_config)


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
def home(page=1):
    twitter = request.environ.get('twitter')
    user = twitter.api.me()
    render_data_list = []
    paginator = None
    if request.params:
        p = request.params.dict
        search_criteria = {
            'since': datetime.datetime.strptime(p['since'][0], '%Y-%m-%d') if p['since'][0] else None,
            'until': datetime.datetime.strptime(p['until'][0], '%Y-%m-%d') if p['until'][0] else None,
            'media_only': 'media_only' in p,
            'screen_name': p['screen_name'][0],
        }

        tweets = search_tweets(search_criteria, selections=['tweet_id'])

        _data_list = utils.fetch_tweet_data(twitter.api, tweets)
        sorted_data = utils.sort_by(p['sort_by'][0], _data_list, reverse=True)

        paginator = utils.Pagination(sorted_data, per_page=10, current_page=page)
        paginated_data = paginator.paginate()

        # Set oEmbded
        render_data_list = []
        for data in paginated_data:
            data['oembed'] = twitter.api.get_oembed(data['tweet_id'])
            render_data_list.append(data)

    return template('home', user=user, data_list=render_data_list, paginator=paginator,
                    query_string=request.query_string, params=request.params)


@route('/import')
def import_csv():
    return template('import')


@route('/import', method='POST')
def do_import_csv():
    twitter = request.environ.get('twitter')
    file = request.files.get('file')
    user = twitter.api.me()
    user_id = user.id
    for data in utils.parse_tweets_csv(codecs.iterdecode(file.file, 'utf8')):
        data['user_id'] = user_id
        create_or_update_tweet(data)
    return redirect('home')


if __name__ == "__main__":
    from models import create_sqlite_table
    create_sqlite_table()
    run(app=app, host="localhost", port=8000, debug=True, reloader=True)

