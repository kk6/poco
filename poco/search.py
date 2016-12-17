# -*- coding: utf-8 -*-
import functools
import operator

from models import Tweet


def search_tweets(search_criteria, selections=None):
    def _build_clauses(criteria):
        _clauses = []
        if criteria['since']:
            _clauses.append(Tweet.timestamp >= criteria['since'])
        if criteria['until']:
            _clauses.append(Tweet.timestamp < criteria['until'])
        if criteria['media_only']:
            _clauses.append(Tweet.expanded_urls.is_null(False))
        if criteria['media_only'] and criteria['screen_name']:
            start = "https://twitter.com/{}/status/".format(criteria['screen_name'])
            end = "/photo/1"
            _clauses.append(Tweet.expanded_urls.startswith(start))
            _clauses.append(Tweet.expanded_urls.endswith(end))
            _clauses.append(~(Tweet.expanded_urls.contains(',')))  # ignore RT/QT
        return functools.reduce(operator.and_, _clauses)

    if selections:
        selections = [getattr(Tweet, field) for field in selections]
        query = Tweet.select(*selections)
    else:
        query = Tweet.select()
    clauses = _build_clauses(search_criteria)
    if clauses:
        query = query.where(clauses)
        print(query)
    for data in query:
        yield data
