# -*- coding: utf-8 -*-
import csv
import datetime


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
