#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 蓝图
@Time       : 2018/7/20 15:50
@Author     : libaojie
@File       : __init__.py
@Software   : PyCharm
"""

from flask import Blueprint, request
from flask_restful import Api
from lbj_common.config_tool import ConfigTool
from lbj_common.log_tool import LogTool
from lbj_flask.user_tool import UserTool


blueprint_authority = Blueprint("api_authority", __name__, url_prefix='/api/vi/api')


@blueprint_authority.before_request
def before_request():
    """
    当前蓝图拦截
    :return:
    """
    if ConfigTool.get_bool('ca', 'IS_AUTH'):

        LogTool.info("authority before_request")
        # 登录权限
        from lbj_flask.filter.auth import Auth
        is_allow, data = Auth.identify_request(request)
        LogTool.info(f"认证结果{is_allow}")
        if is_allow:
            # 认证通过返回当前登录者
            if data is not None:
                UserTool.set_login_user(data)
            return None
        else:
            # 返回错误码
            return data
    else:
        return None
    pass

"""
直接方式
"""
#
from . import normal

"""
restful方式
"""
# api句柄
api_ai = Api(blueprint_authority)

from project.app.api.restful import RestfulRes, RestfulCollRes
api_ai.add_resource(RestfulRes, "/restful")
api_ai.add_resource(RestfulCollRes, "/restfuls")


