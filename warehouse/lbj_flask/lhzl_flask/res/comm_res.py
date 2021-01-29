#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 公共的数据返回类
@Time       : 2020/02/09 13:54
@Author     : libaojie
@File       : comm_res.py
@Software   : PyCharm
"""
import json

from lhzl_common.log_tool import LogTool
from lhzl_db.entity.ret_find import RetFind


class CommRes(object):
    """
    公共的数据返回类
    """

    def __init__(self, enum, data=None):
        """

        :param enum: ErrorCodeImpl
        :param data:
        """
        self.code = enum.get_code()
        self.msg = enum.get_msg()

        if data is None:
            self.data = None
        else:
            if isinstance(data, RetFind):
                self.data = data.data
            else:
                self.data = data

    def test(self):
        LogTool.print(self.code + ":" + self.msg)

    def get_json(self):
        """
        返回格式/中文编码/json序列化
        :param data:
        :return:
        """
        _ret = json.dumps(self, ensure_ascii=False, default=self.obj_2_json)
        return _ret

    def obj_2_json(self, obj):
        """
        对象转json 格式化
        :param obj:
        :return:
        """
        from lhzl_flask.response_tool import ResponseTool
        return {
            "code": obj.code,
            "msg": obj.msg,
            "data": ResponseTool.get_dict_value(obj.data),
        }