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
from middleware.tweepy import TweepyMiddleware

tweepy_config = {
  'consumer_key': os.environ['POCO_CONSUMER_KEY'],
  'consumer_secret': os.environ['POCO_CONSUMER_SECRET'],
  'callback_url': 'http://127.0.0.1:8000/verify',
}
app = TweepyMiddleware(bottle.app(), tweepy_config)


@route('/')
def index():
    return template('index')


@route('/oauth')
def oauth():
    tweepy = request.environ.get('tweepy')
    redirect_url = tweepy.get_authorization_url()
    return redirect(redirect_url)


@route('/verify')
def verify():
    tweepy = request.environ.get('tweepy')
    verifier = request.params.get('oauth_verifier')
    tweepy.authenticate(verifier)
    return redirect('home')


@route('/home')
def home():
    tweepy = request.environ.get('tweepy')
    user = tweepy.api.me()
    return template('home', user=user)


if __name__ == "__main__":
    run(app=app, host="localhost", port=8000, debug=True, reloader=True)
