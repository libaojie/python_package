#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 运行sql结果
@Time       : 2020/02/07 14:23
@Author     : libaojie
@File       : ret_run_sql.py
@Software   : PyCharm
"""


class RetRunSql(object):
    """
    运行sql结果 数据结构
    """

    def __init__(self):
        """
        初始化
        """
        self._is_success = False     # 是否执行成功
        self._col_list = None        # 列名列表
        self._val_list = None        # 返回数据
        pass

    @property
    def is_success(self):
        """
        是否执行成功
        :return:
        """
        return self._is_success

    @is_success.setter
    def is_success(self, _is_success):
        self._is_success = _is_success

    @property
    def col_list(self):
        """
        列名列表
        :return:
        """
        return self._col_list

    @col_list.setter
    def col_list(self, _col_list):
        self._col_list = _col_list

    @property
    def val_list(self):
        """
        返回数据
        :return:
        """
        return self._val_list

    @val_list.setter
    def val_list(self, _val_list):
        self._val_list = _val_list


