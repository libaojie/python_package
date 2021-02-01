#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 文件工具
@Time       : 2020/2/18 16:16
@Author     : libaojie
@File       : file_tool.py
@Software   : PyCharm
"""
import os

from lbj_common.log_tool import LogTool


class FileTool(object):
    """
    文件工具
    """

    @staticmethod
    def get_abspath(rel_path):
        """
        获取绝对路径
        :param path:
        :return:
        """
        return os.path.abspath(rel_path)

    @staticmethod
    def mkdir_file(path):
        """
        创建文件的父菜单
        :param path:
        :return:
        """
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    @staticmethod
    def is_file(rel_path, is_create=True):
        """
        判断文件和文件夹是否存在，不存在自动创建文件夹
        :param rel_path:
        :param is_create:  是否创建
        :return:
        """
        rel_path = FileTool.get_abspath(rel_path)
        if os.path.exists(rel_path):
            LogTool.info("文件路径【%s】存在" % rel_path)
            return True
        else:
            dir_name = os.path.dirname(rel_path)
            if not os.path.exists(dir_name):
                LogTool.info("文件路径【%s】不存在，将自动创建" % rel_path)
                if is_create:
                    FileTool.mkdir_file(dir_name)
                    LogTool.info("路径创建【%s】完成" % dir_name)
        return False

    @staticmethod
    def open_file(rel_path):
        """
        打开文件操作
        :param rel_path: 文件路径
        :return:
        """
        f = None
        content = None
        rel_path = FileTool.get_abspath(rel_path)
        try:
            with open(rel_path, 'r+', encoding='utf8') as f:
                content = f.read()
        except Exception as e:
            LogTool.error(f"打开文件出错：【{e}】")
        finally:
            f.close() if f else None
            return content

    @staticmethod
    def write_file(rel_path):
        """
        写文件
        :param rel_path:
        :return:
        """
        w = None
        rel_path = FileTool.get_abspath(rel_path)
        try:
            w = open(rel_path, 'w+')
            return w
        except Exception as e:
            LogTool.error(f"打开文件出错：【{e}】")
            w.close() if w else None
            return None

    @staticmethod
    def del_file(rel_path):
        """
        删除此路径下所有文件及文件夹
        :param path:
        :return:
        """
        rel_path = FileTool.get_abspath(rel_path)
        if os.path.isdir(rel_path):
            for i in os.listdir(rel_path):
                path_file = os.path.join(rel_path, i)
                FileTool.del_file(path_file)
            # 删除文件夹
            os.rmdir(rel_path)
        elif os.path.isfile(rel_path):
            # 删除文件
            os.remove(rel_path)


