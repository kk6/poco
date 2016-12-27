# -*- coding: utf-8 -*-
import pytest


class TestPagination(object):

    @pytest.fixture
    def target_class(self):
        from poco.pagination import Pagination
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
            (range(30), 10, 1, [1, 2, 3]),
            (range(50), 10, 1, [1, 2, 3, 4, 5]),
            (range(100), 10, 1, [1, 2, 3, 4, 5]),
            (range(100), 10, 2, [1, 2, 3, 4, 5]),
            (range(100), 10, 3, [1, 2, 3, 4, 5]),
            (range(100), 10, 5, [3, 4, 5, 6, 7]),
            (range(100), 10, 7, [5, 6, 7, 8, 9]),
            (range(100), 10, 8, [6, 7, 8, 9, 10]),
            (range(100), 10, 10, [6, 7, 8, 9, 10]),
        ],
    )
    def test_abbreviated_pages(self, target_class, object_list, per_page, current_page, expected):
        p = target_class(object_list, per_page, current_page)
        assert p.abbreviated_pages() == expected

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
