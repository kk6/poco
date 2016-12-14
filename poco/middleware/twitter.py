# -*- coding: utf-8 -*-
""" Tweepy WSGI Middleware
"""
import tweepy


class TwitterManager(object):
    def __init__(self, consumer_key, consumer_secret, access_token=None,
                 access_token_secret=None, callback_url=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.callback_url = callback_url
        self.request_token = None
        self.api = None

    def get_authorization_url(self):
        auth = tweepy.OAuthHandler(self.consumer_key,
                                   self.consumer_secret,
                                   self.callback_url)
        try:
            redirect_url = auth.get_authorization_url()
        except tweepy.TweepError:
            raise tweepy.TweepError('Error! Failed to get request token')
        self.request_token = auth.request_token
        return redirect_url

    def get_access_token(self, verifier):
        auth = tweepy.OAuthHandler(self.consumer_key,
                                   self.consumer_secret)
        if self.request_token is None:
            raise tweepy.TweepError("Request token not set yet.")
        auth.request_token = self.request_token
        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            raise tweepy.TweepError('Error! Failed to get access token')
        return (
            auth.access_token,
            auth.access_token_secret,
        )

    def set_access_token(self, key, secret):
        self.access_token = key
        self.access_token_secret = secret

    def get_oauth_api(self, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(self.consumer_key,
                                   self.consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def set_api(self):
        self.api = self.get_oauth_api(self.access_token, self.access_token_secret)

    def authenticate(self, verifier):
        token = self.get_access_token(verifier)
        self.set_access_token(*token)
        self.set_api()


class TwitterMiddleware(object):

    def __init__(self, app, tweepy_config):
        self.app = app
        self.tweepy_settings = tweepy_config
        self.tweepy_manager = TwitterManager(**self.tweepy_settings)

    def __call__(self, environ, start_response):
        environ['twitter'] = self.tweepy_manager
        return self.app(environ, start_response)

