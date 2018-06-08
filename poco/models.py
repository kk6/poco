# -*- coding: utf-8 -*-
import os
import peewee

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'tweets.db')
db = peewee.SqliteDatabase(DATA_FILE)


def create_sqlite_table():
    if not os.path.exists(DATA_FILE):
        Tweet.create_table()


class Tweet(peewee.Model):
    tweet_id = peewee.IntegerField(primary_key=True)
    in_reply_to_status_id = peewee.IntegerField(null=True)
    in_reply_to_user_id = peewee.IntegerField(null=True)
    timestamp = peewee.DateTimeField()
    text = peewee.TextField()
    retweeted_status_id = peewee.IntegerField(null=True)
    retweeted_status_user_id = peewee.IntegerField(null=True)
    retweeted_status_timestamp = peewee.DateTimeField(null=True)
    expanded_urls = peewee.TextField(null=True)
    user_id = peewee.IntegerField()

    class Meta:
        database = db


def get_or_create_tweet(data):
    try:
        tweet = Tweet.get_by_id(data["tweet_id"])
    except Tweet.DoesNotExist:
        tweet = Tweet.create(**data)
    return tweet
