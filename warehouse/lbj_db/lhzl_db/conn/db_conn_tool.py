#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : oracle链接工具
@Time       : 2019/3/21 9:30
@Author     : libaojie
@File       : db_conn_tool.py
@Software   : PyCharm
"""
import cx_Oracle


class DBConnTool(object):
    """
    数据库链接字符串 拼装
    """

    @classmethod
    def get_oracle_conn_str(cls, ip, port, uname, pwd, sid=None, service_name=None):
        """
        获取oracle链接字符串
        :param ip:
        :param port:
        :param uname:
        :param pwd:
        :param sid:
        :param service_name:
        :return:
        """
        if sid is not None:
            return f"oracle://{uname}:{pwd}@{ip}:{port}/{sid}"
        if service_name is not None:
            dsnStr = cx_Oracle.makedsn(ip, port, service_name=service_name)
            return f"oracle://{uname}:{pwd}@{dsnStr}"
        return None

    @classmethod
    def get_mysql_conn_str(cls, ip, port, uname, pwd, dbname):
        """
        获取mysql的连接字符串
        :param ip:
        :param port:
        :param uname:
        :param pwd:
        :param dbname:
        :return:
        """
        return f"mysql+pymysql://{uname}:{pwd}@{ip}:{port}/{dbname}"

