#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 公共数据
@Time       : 2020/02/19 17:05
@Author     : libaojie
@File       : model.py
@Software   : PyCharm
"""


class CommData(object):
    """
    公共数据
    """

    def __init__(self):
        """
        初始化
        """
        self._pro_name = None  # 项目名称

    @property
    def pro_name(self):
        """
        当前项目名称
        :return:
        """
        return self._pro_name

    @pro_name.setter
    def pro_name(self, _pro_name):
        self._pro_name = _pro_name
