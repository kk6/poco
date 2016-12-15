# -*- coding: utf-8 -*-
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
    dir_path = os.path.join('/tmp', user.id_str)
    path = os.path.join(dir_path, 'tweets.csv')
    data_list = []
    paginator = None
    if os.path.exists(path):
        parser = utils.TweetsCsvParser(path, screen_name=user.screen_name)
        media_tweets = parser.filter_images_by_since('2016-01-01 00:00:00 +0900')
        _data_list = utils.fetch_tweet_data(twitter.api, media_tweets)
        sorted_data = utils.sort_by('likes', _data_list, reverse=True)
        paginator = utils.Pagination(sorted_data, per_page=10, current_page=page)
        paginated_data = paginator.paginate()
        for data in paginated_data:
            data['oembed'] = twitter.api.get_oembed(data['tweet_id'])
            data_list.append(data)
    return template('home', user=user, data_list=data_list, paginator=paginator)


@route('/import')
def import_csv():
    return template('import')


@route('/import', method='POST')
def do_import_csv():
    twitter = request.environ.get('twitter')
    user = twitter.api.me()
    dir_path = os.path.join('/tmp', user.id_str)
    os.makedirs(dir_path, exist_ok=True)
    file = request.files.get('file')
    file.save(dir_path, overwrite=True)
    return redirect('home')


if __name__ == "__main__":
    run(app=app, host="localhost", port=8000, debug=True, reloader=True)

