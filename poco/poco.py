# -*- coding: utf-8 -*-
import os

import tweepy
import bottle
from bottle import (
    route,
    run,
    TEMPLATE_PATH,
    jinja2_template as template,
    redirect,
    request,
)
from beaker.middleware import SessionMiddleware

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.append(BASE_DIR + "/views")
CALLBACK_URL = 'http://127.0.0.1:8000/verify'

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)


@route('/')
def index():
    return template('index')


@route('/oauth')
def oauth():
    auth = tweepy.OAuthHandler(
        os.environ['POCO_CONSUMER_KEY'],
        os.environ['POCO_CONSUMER_SECRET'],
        CALLBACK_URL,
    )
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        raise tweepy.TweepError('Error! Failed to get request token')
    s = bottle.request.environ.get('beaker.session')
    s['request_token'] = auth.request_token
    s.save()
    return redirect(redirect_url)


@route('/verify')
def verify():
    verifier = request.params.get('oauth_verifier')
    auth = tweepy.OAuthHandler(
        os.environ['POCO_CONSUMER_KEY'],
        os.environ['POCO_CONSUMER_SECRET'],
    )
    s = bottle.request.environ.get('beaker.session')
    try:
        token = s['request_token']
    except KeyError:
        return redirect('/')
    del s['request_token']

    auth.request_token = token
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        raise tweepy.TweepError('Error! Failed to get access token')
    s['access_token'] = auth.access_token
    s['access_token_secret'] = auth.access_token_secret
    return redirect('home')


@route('/home')
def home():
    auth = tweepy.OAuthHandler(
        os.environ['POCO_CONSUMER_KEY'],
        os.environ['POCO_CONSUMER_SECRET'],
    )
    try:
        s = request.environ['beaker.session']
    except KeyError:
        return redirect('/')
    auth.set_access_token(
        s['access_token'],
        s['access_token_secret'],
    )
    api = tweepy.API(auth)
    user = api.me()
    return template('home', user=user)


if __name__ == "__main__":
    run(app=app, host="localhost", port=8000, debug=True, reloader=True)

