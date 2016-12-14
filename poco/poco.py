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
def home():
    twitter = request.environ.get('twitter')
    user = twitter.api.me()
    return template('home', user=user)


if __name__ == "__main__":
    run(app=app, host="localhost", port=8000, debug=True, reloader=True)
