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

    ret = input('等待输入')
    LogTool.print(f"hello world 【{ret}】")


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
        from lbj_common.log_tool import LogTool

        LogTool.error(traceback.format_exc())
