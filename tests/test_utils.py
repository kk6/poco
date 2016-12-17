# -*- coding: utf-8 -*-
from datetime import datetime, timezone, timedelta

import pytest


class TestStr2Datetime(object):
    @pytest.fixture
    def target_func(self):
        from poco.utils import str2datetime
        return str2datetime

    @pytest.mark.parametrize(
        's,expected',
        [
            ('2016-01-01 00:00:00 +0900',
             datetime(2016, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(0, 32400)))),
            ('', None),
        ],
    )
    def test_call(self, target_func, s, expected):
        assert target_func(s) == expected

    @pytest.mark.parametrize('non_str_value', [None, 1, object])
    def test_type_error(self, target_func, non_str_value):
        with pytest.raises(TypeError):
            target_func(non_str_value)


class TestPagination(object):

    @pytest.fixture
    def target_class(self):
        from poco.utils import Pagination
        return Pagination

    @pytest.mark.parametrize(
        'object_list, per_page, current_page, expected',
        [
            (range(101), 10, 1, 11),
            (range(1), 20, 1, 1),
            (range(55), 20, 2, 3),
        ],
    )
    def test_pages(self, target_class, object_list, per_page, current_page, expected):
        p = target_class(object_list, per_page, current_page)
        assert p.pages == expected

    @pytest.mark.parametrize(
        'object_list, per_page, current_page, expected',
        [
            (range(101), 10, 1, False),
            (range(101), 10, 11, True),
            (range(55), 20, 1, False),
            (range(55), 20, 2, True),
            (range(55), 20, 3, True),
        ],
    )
    def test_has_prev(self, target_class, object_list, per_page, current_page, expected):
        p = target_class(object_list, per_page, current_page)
        assert p.has_prev is expected

    @pytest.mark.parametrize(
        'object_list, per_page, current_page, expected',
        [
            (range(101), 10, 1, True),
            (range(101), 10, 11, False),
            (range(55), 20, 1, True),
            (range(55), 20, 2, True),
            (range(55), 20, 3, False),
        ],
    )
    def test_has_next(self, target_class, object_list, per_page, current_page, expected):
        p = target_class(object_list, per_page, current_page)
        assert p.has_next is expected

    @pytest.mark.parametrize(
        'object_list, per_page, current_page, expected',
        [
            (range(101), 10, 1, None),
            (range(101), 10, 11, 10),
            (range(55), 20, 1, None),
            (range(55), 20, 2, 1),
            (range(55), 20, 3, 2),
        ],
    )
    def test_prev_page(self, target_class, object_list, per_page, current_page, expected):
        p = target_class(object_list, per_page, current_page)
        assert p.prev_page == expected

    @pytest.mark.parametrize(
        'object_list, per_page, current_page, expected',
        [
            (range(101), 10, 1, 2),
            (range(101), 10, 11, None),
            (range(55), 20, 1, 2),
            (range(55), 20, 2, 3),
            (range(55), 20, 3, None),
        ],
    )
    def test_next_page(self, target_class, object_list, per_page, current_page, expected):
        p = target_class(object_list, per_page, current_page)
        assert p.next_page == expected

    @pytest.mark.parametrize(
        'object_list, per_page, current_page, expected',
        [
            (range(101), 10, 1, range(10)),
            (range(101), 10, 11, range(100, 101)),
            (range(55), 20, 1, range(20)),
            (range(55), 20, 2, range(20, 40)),
            (range(55), 20, 3, range(40, 55)),
        ],
    )
    def test_paginate(self, target_class, object_list, per_page, current_page, expected):
        p = target_class(object_list, per_page, current_page)
        assert p.paginate() == expected
