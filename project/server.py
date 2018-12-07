#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 程序主入口
@Time       : 2018/5/17 9:50
@Author     : libaojie
@File       : server.py
@Software   : PyCharm
"""
import os
import platform
import sys
import traceback

from project import config
from project.app.plugins.log_tool import LogTool

try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(approot)[0])


from project.app.core.close_task import close_task

def __init_log():
    # 初始化日志模块
    log_path = os.path.abspath(os.path.join(approot, config.LOG))
    LogTool.init(log_path)
    LogTool.print(f"日志路径:{log_path}")
    pass


def __run():
    # 设计中文环境变量
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    # 初始化日志模块
    __init_log()

    close_task()

    input('等待输入')


if __name__ == '__main__':

    try:
        if 'Windows' in platform.platform():
            __run()
        elif 'Linux' in platform.platform():
            __run()
        else:
            print('无法识别平台！{0}'.format())
            os._exit(0)
    except Exception as err:
        LogTool.error(traceback.format_exc())
