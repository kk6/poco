# -*- coding: utf-8 -*-
import csv
import datetime
import math


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


def force_int(s):
    """Forcibly convert to int

    :param s: any python object
    :return: int or None
    """
    try:
        return int(s)
    except ValueError:
        return None


def parse_tweets_csv(fp):
    """Parse tweets.csv and convert the value to a Python object
    """
    for row in csv.DictReader(fp):
        yield {
            'tweet_id': force_int(row['tweet_id']),
            'in_reply_to_status_id': force_int(row['in_reply_to_status_id']),
            'in_reply_to_user_id': force_int(row['in_reply_to_user_id']),
            'timestamp': str2datetime(row['timestamp']),
            'text': row['text'],
            'retweeted_status_id': force_int(row['retweeted_status_id']),
            'retweeted_status_user_id': force_int(row['retweeted_status_user_id']),
            'retweeted_status_timestamp': str2datetime(row['retweeted_status_timestamp']),
            'expanded_urls': row['expanded_urls'],
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
        """Returns a sub sequence of object_list
        """
        start = (self.current_page - 1) * self.per_page
        end = start + self.per_page
        return self.object_list[start:end]
