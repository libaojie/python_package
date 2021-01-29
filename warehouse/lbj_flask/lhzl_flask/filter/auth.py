#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2018/10/9 11:40
@Author     : libaojie
@File       : auth.py
@Software   : PyCharm
"""
import time
import urllib.parse

from lhzl_common.config_tool import ConfigTool
from lhzl_common.decorator import except_fun
from lhzl_common.log_tool import LogTool
from flask import jsonify

from lhzl_flask.common import constant
from lhzl_flask.enum.error_code import ErrorCode
from lhzl_flask.http_tool import HttpTool
from lhzl_flask.ip_tool import IpTool
from lhzl_flask.res.comm_res import CommRes
from lhzl_flask.response_tool import ResponseTool


class Auth(object):


    @classmethod
    @except_fun
    def identify_request(cls, request):
        """
        用户鉴权
        :return: True,None/False,errorcode
        """
        LogTool.info("用户鉴权")
        if request is None:
            return False, ResponseTool.get_json_ret(CommRes(ErrorCode.HAVE_NOT_REQ))

        request.__setattr__(constant.lhzl_Time_Begin, time.localtime())

        userId = request.headers.get(constant.USERID)
        user = request.headers.get(constant.USERNAME)
        userName = urllib.parse.unquote(user) if user is not None else ""
        loginName = request.headers.get(constant.LOGINNAME)
        sysLogId = request.headers.get(constant.SYSLOGID)
        msg = request.headers.get(constant.MSG)

        if userId is None or userName is None or loginName is None \
                or len(userId) == 0 or len(userName) == 0 or len(loginName) == 0:
            ipAddress = IpTool.get_ip(request)
            LogTool.info('鉴权接口：ip:【{3}】 url:【{0}】 model:【{1}】 value:【{2}】'.format(request.path, request.method,
                                                                                  request.values.__str__(), ipAddress))
            auth_url = ConfigTool.get_str('ca', 'AUTHORITY_URL')
            auth_header = request.headers.get(constant.Authorization)
            appId = request.headers.get(constant.Application)
            # 实际上 header中的参数是不区分大小写的
            authUserName = request.headers.get(constant.AuthUserName)
            password = request.headers.get(constant.AuthPassword)
            appCode = request.headers.get(constant.ApplicationCode)
            userAgent = request.headers[constant.UserAgent]  # 获取 浏览器信息
            headers = {constant.Authorization: auth_header, constant.Application: appId, constant.UserAgent: userAgent,
                       constant.AuthUserName: authUserName, constant.AuthPassword: password, constant.ApplicationCode: appCode}
            payload = {'ip': ipAddress, 'url': request.path, 'type': request.method}

            val = HttpTool.request_get(auth_url, payload, headers)
            if val is not None:
                if val['code'] == '0':
                    # 鉴权成功
                    # UserTool.set_login_user(val['data'])
                    return True, val['data']
                else:
                    # 鉴权失败
                    return False, jsonify(val)
            return False, jsonify(val)
        else:
            LogTool.info('* 已鉴权 *')
            return True, {constant.USERID:userId, constant.USERNAME: userName, constant.LOGINNAME:loginName}

