#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/3/21 9:30
@Author     : libaojie
@File       : http_tool.py
@Software   : PyCharm
"""
import json

import requests
from lhzl_common.log_tool import LogTool
from flask import request


class HttpTool(object):

    @staticmethod
    def request_get(url, payload, headers=None):
        """
        请求get
        :param url:
        :param payload:
        :return:
        """

        LogTool.info(f"网络get发包：url:【{url}】, payload：【{payload}】")
        auth_header = request.headers.get('Authorization')
        appCode = request.headers.get('Application')
        if headers is None:
            headers = {}
        if not headers.__contains__('Authorization'):
            headers['Authorization'] = auth_header
        if not headers.__contains__('Application'):
            headers['Application'] = appCode

        val = None
        respone = requests.get(url, headers=headers, params=payload)
        LogTool.info(f"网络get收包：respone:【{str(respone)}】")
        if respone.status_code == 200:
            val = json.loads(respone.text)
            LogTool.info(f"网络包解析:【{val}】")
        return val

    @staticmethod
    def request_post(url, payload,headers=None):
        """
        请求post
        :param url:
        :param payload:
        :return:
        """
        LogTool.info(f"网络post发包：url:【{url}】, payload：【{payload}】")
        auth_header = request.headers.get('Authorization')
        appCode = request.headers.get('Application')
        if headers is None:
            headers = {}
        if not headers.__contains__('Authorization'):
            headers['Authorization'] = auth_header
        if not headers.__contains__('Application'):
            headers['Application'] = appCode

        val = None
        respone = requests.post(url, headers=headers, json=payload)
        LogTool.info(f"网络get收包：respone:【{str(respone)}】")
        if respone.status_code == 200:
            val = json.loads(respone.text)
            LogTool.info(f"网络包解析:【{val}】")
        return val
