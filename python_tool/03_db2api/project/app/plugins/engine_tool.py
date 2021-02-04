#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/9/23 16:16
@Author     : libaojie
@File       : engine_tool.py
@Software   : PyCharm
"""
from sqlalchemy import create_engine


class EngineTool(object):
    """
    连接方式为Engine
    """

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    @classmethod
    def get_engine(cls, owner):

        # 数据库用户和密码
        k_v ={"ca":"pw"
              }
        engine = create_engine(f'oracle://{owner}:{k_v[owner]}@ip:port/orcl')
        return engine
