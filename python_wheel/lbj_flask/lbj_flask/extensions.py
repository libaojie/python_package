#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2018/7/2 14:56
@Author     : libaojie
@File       : extensions.py
@Software   : PyCharm
"""
from flask_sqlalchemy import SQLAlchemy

from lhzl_flask.common.comm_data import CommData

# 打包引入，缺模块
import sqlalchemy.sql.default_comparator

# 系统常量
commData = CommData()
# Flask数据库
db = SQLAlchemy(session_options={"autoflush": False, "autocommit": False})
