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

try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(approot)[0])


def __run():
    # 设计中文环境变量
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

    input('等待输入')

    # import tkinter.filedialog
    # 选中文件夹
    # _path = tkinter.filedialog.askdirectory()
    # if _path == '':
    #     print("请选择正确的文件夹路径！")
    #     return

    # _path = tkinter.filedialog.askopenfilename(filetypes=[("JSON文件", "*.json;*.xlsx")])
    # if _path == '':
    #   print("请选择正确的json路径！")
    #    return


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
        print(traceback.format_exc())
