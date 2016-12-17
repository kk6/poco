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
