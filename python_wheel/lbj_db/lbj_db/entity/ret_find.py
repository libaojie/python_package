#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 查询sql列表结果
@Time       : 2020/02/08 20:47
@Author     : libaojie
@File       : ret_find.py
@Software   : PyCharm
"""


class RetFind(object):
    """
    查询列表结果
    """

    def __init__(self):
        self._page_size = None   # 当前页面
        self._page_num = None   # 每页数量
        self._page_total = None  # 一共页数
        self._total = None       # 数据总量
        self._data = None        # 数据列表

    @property
    def page_size(self):
        """
        当前页面
        :return:
        """
        return self._page_size

    @page_size.setter
    def page_size(self, _page_size):
        self._page_size = _page_size

    @property
    def page_num(self):
        """
        每页数量
        :return:
        """
        return self._page_num

    @page_num.setter
    def page_num(self, _page_num):
        self._page_num = _page_num

    @property
    def page_total(self):
        """
        一共页数
        :return:
        """
        return self._page_total

    @page_total.setter
    def page_total(self, _page_total):
        self._page_total = _page_total

    @property
    def data(self):
        """
        数据列表
        :return:
        """
        return self._data

    @data.setter
    def data(self, _data):
        self._data = _data

    @property
    def total(self):
        """
        数据总数量
        :return:
        """
        return self._total

    @total.setter
    def total(self, _total):
        self._total = _total