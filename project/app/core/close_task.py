#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 关闭某些进程
@Time       : 2018/5/22 15:41
@Author     : libaojie
@File       : close_task.py
@Software   : PyCharm
"""
import os


def close_task():
    """
    关闭某些进程
    :return:
    """
    command = 'taskkill /F /IM python.exe'
    os.system(command)
    pass


# close_task()
