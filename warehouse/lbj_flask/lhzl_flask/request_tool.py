#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 请求工具
@Time       : 2019/2/28 9:18
@Author     : libaojie
@File       : request_tool.py
@Software   : PyCharm
"""
from lbj_common.config_tool import ConfigTool
from lbj_common.log_tool import LogTool
from lbj_common.type_tool import TypeTool
from flask import request

from lbj_flask.enum.error_code import ErrorCode
from lbj_flask.res.comm_res import CommRes
from lbj_flask.response_tool import ResponseTool


class RequestTool(object):

    @staticmethod
    def handle_request():
        """
        预处理request
        :return:
        """
        LogTool.info("----------请求开始----------")
        if request is None:
            LogTool.error('前端未发送request！')
            return ResponseTool.get_json_ret(CommRes(ErrorCode.REQ_IS_NONE))

        LogTool.info(f'url:【{request.path}】 model:【{request.method}】')

        if request.path not in ConfigTool.get_list('ignore', 'IGNORE_URL'):
            # POST、PUT方式必须以json方式提交
            if request.method in ['POST', 'PUT']:
                if not 'application/json' in request.content_type:
                    LogTool.error(f"数据传输格式有误！ method:【{request.method}】 content_type:【{request.content_type}】")
                    return ResponseTool.get_json_ret(CommRes(ErrorCode.HEADER_TYPE_SETTING))
                else:
                    try:
                        json = request.json
                    except Exception as err:
                        LogTool.error(f"传输的json格式有误【{request.data}】")
                        return ResponseTool.get_json_ret(CommRes(ErrorCode.JSON_ERROR))

                LogTool.info(f'value:【{request.json}】')
            else:
                LogTool.info(f'value:【{request.args}】')
        return None

    @staticmethod
    def get_request_page(request):
        """
        获取分页信息
        :param request:
        :return:
        """
        page_num = request.args.get('pageNum')
        page_size = request.args.get('pageSize')

        page_num = TypeTool.change_to_int(page_num)
        page_size = TypeTool.change_to_int(page_size)
        return page_num, page_size
