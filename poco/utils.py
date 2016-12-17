# -*- coding: utf-8 -*-
import csv
import datetime
import itertools
import math

import arrow


def str2datetime(s):
    """Datetime strings to datetime object

    :param str s: datetime string
    :rtype: datetime
    :return: datetime object. If an empty string is received, None is returned.
    """
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S %z')
    except ValueError:
        return None


class TweetsCsvParser(object):
    def __init__(self, path, screen_name):
        self.path = path
        self.screen_name = screen_name

    def filter_images_by_since(self, since):
        since = str2datetime(since)
        with open(self.path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = "https://twitter.com/{screen_name}/status/{tweet_id}/photo/1".format(
                    screen_name=self.screen_name,
                    tweet_id=row['tweet_id'],
                )
                if url == row['expanded_urls']:
                    if since <= str2datetime(row['timestamp']):
                        yield row


def fetch_tweet_data(api, media_tweets, text_trancate_to=30):
    itr = iter(media_tweets)
    while 1:
        sub_iter = itertools.islice(itr, 100)
        tweet_ids = [r['tweet_id'] for r in sub_iter]
        if not tweet_ids:
            break
        tweets = api.statuses_lookup(tweet_ids)
        for tweet in tweets:
            yield {
                'tweet_id': tweet.id,
                'likes': tweet.favorite_count,
                'retweets': tweet.retweet_count,
                'text': tweet.text.replace('\n', '')[:text_trancate_to],
                'created_at': arrow.get(tweet.created_at).to('JST').format('MM/DD HH:mm'),
            }


def sort_by(key, data_list, reverse=False):
    return sorted(data_list, key=lambda d: d[key], reverse=reverse)


class Pagination(object):

    def __init__(self, object_list, per_page, current_page):
        self.object_list = object_list
        self.per_page = per_page
        self.current_page = current_page
        self.total_count = len(object_list)

    @property
    def pages(self):
        return math.ceil(self.total_count / self.per_page)

    @property
    def has_prev(self):
        return self.current_page > 1

    @property
    def has_next(self):
        return self.current_page < self.pages

    @property
    def prev_page(self):
        if self.has_prev:
            return self.current_page - 1

    @property
    def next_page(self):
        if self.has_next:
            return self.current_page + 1

    def paginate(self):
        start = (self.current_page - 1) * self.per_page
        end = start + self.per_page
        return self.object_list[start:end]
