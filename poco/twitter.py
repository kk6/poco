# -*- coding: utf-8 -*-
import itertools

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock',
    'cache.regions': 'long_term, oembed',
    'cache.long_term.type': 'file',
    'cache.long_term.expire': '86400',
    'cache.oembed.type': 'file',
    'cache.oembed.expire': '3153600000',
}

cache = CacheManager(**parse_cache_config_options(cache_opts))


@cache.region('long_term')
def _cached_statuses_lookup(api, tweet_ids):
    return _statuses_lookup(api, tweet_ids)


def _statuses_lookup(api, tweet_ids):
    return api.statuses_lookup(tweet_ids, trim_user=True)


def fetch_tweet_data(api, tweets):
    itr = iter(tweets)
    while 1:
        sub_iter = itertools.islice(itr, 100)
        tweet_ids = [t.tweet_id for t in sub_iter]
        if not tweet_ids:
            break
        try:
            _tweets = _cached_statuses_lookup(api, tweet_ids)
        except EOFError:
            _tweets = _statuses_lookup(api, tweet_ids)
        for tweet in _tweets:
            yield {
                'tweet_id': tweet.id,
                'likes': tweet.favorite_count,
                'retweets': tweet.retweet_count,
            }


@cache.region('oembed')
def get_cached_oembed(api, tweet_id):
    return get_oembed(api, tweet_id)


def get_oembed(api, tweet_id):
    return api.get_oembed(tweet_id)
