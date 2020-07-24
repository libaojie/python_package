#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 响应工具
@Time       : 2019/2/28 9:21
@Author     : libaojie
@File       : response_tool.py
@Software   : PyCharm
"""
import os
from datetime import datetime
from urllib.parse import quote

from lhzl_common.log_tool import LogTool
from lhzl_common.time_tool import TimeTool
from lhzl_db.entity.ret_find import RetFind
from flask import json, Response, make_response, send_from_directory

from lhzl_flask.enum.error_code import ErrorCode
from lhzl_flask.res.comm_res import CommRes
from lhzl_flask.res.page_res import PageRes


class ResponseTool(object):

    @staticmethod
    def handle_response(response):
        """
        最后处理response
        :return:
        """
        from lhzl_db.db_session_tool import DBSessionTool

        LogTool.info(f"请求结束，状态码【{response.status_code}】")
        if response.status_code == 200:
            if response.is_streamed:
                # 文件流处理
                LogTool.info("此为文件处理！")
                DBSessionTool.commit()
                return response
            val = json.loads(response.data)
            if val is None:
                return ResponseTool.get_json_ret(CommRes(ErrorCode.FAILURE))
            if val.__contains__('code') and val['code'] == '0' and not DBSessionTool.commit():
                return ResponseTool.get_json_ret(CommRes(ErrorCode.DB_ERROR))
        LogTool.info(f"##########请求结束##################")
        return response

    @staticmethod
    def get_json_ret(data):
        """
        返回json
        :param data:
        :return: Response
        """
        _ret = None
        if data is not None:

            # 基本类型处理
            from lhzl_flask.entity.entity_base import EntityBase
            if isinstance(data, dict) or isinstance(data, list) or isinstance(data, str) or isinstance(data,
                                                                                                       EntityBase):
                data = CommRes(ErrorCode.SUCCESS, data=data)

            # find sql 查询结果
            if isinstance(data, RetFind):
                if data.page_num:
                    # 有分页
                    data = PageRes(ErrorCode.SUCCESS, data=data)
                else:
                    # 无分页
                    data = CommRes(ErrorCode.SUCCESS, data=data)

            # 公共返回结构
            if isinstance(data, CommRes):
                _ret = data.get_json()
            else:
                LogTool.error(f"无法识别返回数据结构！{data}")
                _ret = "无法识别返回数据结构"

        return Response(_ret, mimetype='application/json')

    @staticmethod
    def get_dict_value(param):
        """
        获取字典值
        :param param:
        :return:
        """
        from lhzl_flask.entity.entity_base import EntityBase

        def _f(param):
            if param is None:
                return ''
            elif isinstance(param, str):
                return param
            elif isinstance(param, int):
                return param
            elif isinstance(param, datetime):
                return TimeTool.get_std_time(param)
            elif isinstance(param, dict):
                ret = {}
                for key, val in param.items():
                    ret[key] = _f(val)
                return ret
            elif isinstance(param, list):
                return [_f(val) for val in param]
            elif isinstance(param, EntityBase):
                return _f(param.as_dict())

        return _f(param)

    @staticmethod
    def download_file(fpath):
        """
        下载文件
        :param fpath:
        :return:
        """
        if not os.path.exists(fpath):
            LogTool.error(f'文件目录不存在：【{fpath}】')
            return ResponseTool.get_json_ret(CommRes(ErrorCode.FILE_PATH_NOT_EXISTS, data=fpath))  # 文件目录不存在

        if os.path.isfile(fpath):
            try:
                filepath, fullflname = os.path.split(fpath)  # 分割目录和文件名
                LogTool.info(f'文件目录为：【{filepath}】文件名为：【{fullflname}】')
                response = make_response(send_from_directory(filepath, fullflname, as_attachment=True))
                # 解决同一个文件下载url下，google缓存问题，
                # 该问题曾导致修改上传文件后，下载还是最初始的文件问题。
                response.headers["Cache-Control"] = "no-store"
                response.headers["Content-Disposition"] = "attachment; filename={}".format(
                    quote(fullflname))
                return response
            except Exception as err:
                LogTool.error(f"下载文件出错【{str(err)}】")
                return ResponseTool.get_json_ret(CommRes(ErrorCode.FILE_DOWNLOAD_FAILURE))
        else:
            LogTool.error('非文件！请确认文件路径')
            return ResponseTool.get_json_ret(CommRes(ErrorCode.FILE_IS_NONE))  # 不是文件
