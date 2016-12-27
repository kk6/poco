# -*- coding: utf-8 -*-
import math


class Pagination(object):

    def __init__(self, object_list, per_page, current_page, abbreviated_page_count=5):
        self.object_list = object_list
        self.per_page = per_page
        self.current_page = current_page
        self.total_count = len(object_list)
        self.abbreviated_page_count = abbreviated_page_count

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

    def abbreviated_pages(self):
        """Returns an abbreviated page set centered on the current page

        :return: abbreviated pages

        """
        left_margin = self.abbreviated_page_count // 2
        right_margin = self.abbreviated_page_count // 2 + 1

        if self.pages > self.abbreviated_page_count:
            if self.current_page <= left_margin:
                pages = range(1, self.abbreviated_page_count + 1)
            elif (self.current_page + right_margin) <= self.pages:
                pages = range(self.current_page - left_margin,
                              self.current_page + right_margin)
            else:
                pages = range(self.pages - (self.abbreviated_page_count - 1),
                              self.pages + 1)
        else:
            pages = range(1, self.pages + 1)
        return list(pages)

    def paginate(self):
        """Returns a sub sequence of object_list
        """
        start = (self.current_page - 1) * self.per_page
        end = start + self.per_page
        return self.object_list[start:end]
