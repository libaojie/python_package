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
import tkinter.filedialog
import traceback

from lbj_common.config_tool import ConfigTool
from lbj_common.log_tool import LogTool

try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(approot)[0])
ConfigTool.set_path(approot)


def __init_env():
    """
    初始化环境
    :return:
    """
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def __init_log():
    """
    初始化日志模块
    :return:
    """
    log_path = os.path.abspath(os.path.join(ConfigTool.get_path(), ConfigTool.get_str("log", "LOG")))
    LogTool.init(log_path)


def __run():
    __init_env()
    __init_log()

    from project.demo1 import TFDemo
    tfDemo = TFDemo()
    tfDemo.main()

    # from project.demo2 import TFDemo2
    # tfDemo = TFDemo2()
    # tfDemo.main()



if __name__ == '__main__':
    try:
        __run()
        # input("")
    except Exception as err:
        from lbj_common.log_tool import LogTool
        LogTool.print(traceback.format_exc())
