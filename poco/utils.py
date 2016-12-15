# -*- coding: utf-8 -*-
import csv
import itertools

import arrow


def timestamp2arrow(timestamp):
    return arrow.get(timestamp, 'YYYY-MM-DD HH:mm:ss Z')


class TweetsCsvParser(object):
    def __init__(self, path, screen_name):
        self.path = path
        self.screen_name = screen_name

    def filter_images_by_since(self, since):
        with open(self.path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if timestamp2arrow(since) <= timestamp2arrow(row['timestamp']):
                    url = "https://twitter.com/{screen_name}/status/{tweet_id}/photo/1".format(
                        screen_name=self.screen_name,
                        tweet_id=row['tweet_id'],
                    )
                    if url == row['expanded_urls']:
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
