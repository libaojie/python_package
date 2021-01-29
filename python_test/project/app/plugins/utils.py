#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 工具箱
@Time       : 2018/7/20 16:20
@Author     : libaojie
@File       : utils.py
@Software   : PyCharm
"""
import datetime
import time
import uuid

from project.app.common import constant
from project.app.plugins.log_tool import LogTool


class Utils(object):
    """
    工具类
    """

    @staticmethod
    def change_to_int(numb):
        """
        转化为int
        :param numb:
        :return:
        """
        _result = None

        if isinstance(numb, str) or isinstance(numb, float):
            try:
                _result = int(numb)
            except Exception as e:
                LogTool.error("{0}转int失败：{1}".format(type(numb), numb))
            finally:
                return _result

        return _result

    @staticmethod
    def is_null(val):
        '''
        检测不明类型是否为空
        :param val:
        :return:
        '''
        if val is None:
            return True

        if isinstance(val, str) and val.strip() == '':
            return True

        if isinstance(val, list) and len(val) == 0:
            return True

        return False
