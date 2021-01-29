#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    :
@Time       : 2019/8/16 9:57
@Author     : libaojie
@File       : user_tool.py
@Software   : PyCharm
"""
from lhzl_common.log_tool import LogTool
from flask import g

from lhzl_flask.common import constant


class UserTool(object):
    """
    当前登陆用户相关操作
    """

    @staticmethod
    def get_login_user():
        """
        获取当前登录用户
        :return:
        """
        try:
            if hasattr(g, 'user'):
                user = getattr(g, 'user', None)
                return user
            return None
        except Exception as e:
            return None

    @staticmethod
    def set_login_user(user):
        """
        设置当前用户
        :param user:
        :return:
        """
        g.user = user
        LogTool.info(f"全局用户：{g.user}")

    @staticmethod
    def get_login_name():
        """
        获取当前登录用户登录名
        :return:
        """
        user = UserTool.get_login_user()
        if user is not None and g.user.__contains__(constant.LOGINNAME):
            return g.user.get(constant.LOGINNAME)
        return ''

    @staticmethod
    def get_user_name():
        """
        获取当前登录用户用户名
        :return:
        """
        user = UserTool.get_login_user()
        if user is not None and g.user.__contains__(constant.USERNAME):
            return g.user.get(constant.USERNAME)
        return ''

    @staticmethod
    def get_user_id():
        """
        获取当前登录用户id
        :return:
        """
        user = UserTool.get_login_user()
        if user is not None and g.user.__contains__(constant.USERID):
            return g.user.get(constant.USERID)
        return ''
