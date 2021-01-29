#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 分页的数据返回类
@Time       : 2020/02/09 13:56
@Author     : libaojie
@File       : page_res.py
@Software   : PyCharm
"""
import json

from lbj_common.log_tool import LogTool
from lbj_db.entity.ret_find import RetFind

from lbj_flask.res.comm_res import CommRes


class PageRes(CommRes):
    """
    分页的数据返回类
    """

    def __init__(self, enum, data=None):
        """

        :param enum: ErrorCodeImpl
        :param data:
        """
        super(PageRes, self).__init__(enum, data=data)
        if data is not None and isinstance(data, RetFind):
            self.total = data.total
            self.page_total = data.page_total
            self.page_num = data.page_num
            self.per_page = data.page_size
        else:
            self.total = None
            self.page_total = None
            self.page_num = None
            self.per_page = None

    def test(self):
        LogTool.print(self.code + ":" + self.msg + "," + self.total + "," + self.per_page)

    def get_json(self):
        """
        返回格式/中文编码/json序列化
        :param data:
        :return:
        """
        _ret = json.dumps(self, ensure_ascii=False, default=self.obj_2_json)
        return _ret

    def obj_2_json(self, obj):
        from lbj_flask.response_tool import ResponseTool
        return {
            "code": obj.code,
            "msg": obj.msg,
            "data": ResponseTool.get_dict_value(obj.data),
            "total": obj.total,
            "pageSize": obj.per_page,
            "pageNum": obj.page_num
        }
