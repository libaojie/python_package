#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 配置类
@Time       : 2019/5/20 15:46
@Author     : libaojie
@File       : config_tool.py
@Software   : PyCharm
"""
import configparser
import os
import sys


class ConfigTool(object):
    """
    配置类
    """
    __config_dic = {}
    __pro_path = None
    __path = None

    __model_dic = {}

    @classmethod
    def set_path(cls, path):
        """
        设置根路径
        :param path:
        :return:
        """
        if cls.__pro_path is None:
            # 系统根
            approot = os.path.split(path)[0]
            if approot not in sys.path:
                sys.path.append(approot)

            cls.__pro_path = path

    @classmethod
    def get_path(cls):
        """
        获取根路径
        :return:
        """
        return cls.__pro_path

    @classmethod
    def __get_config(cls, sector, item):
        """
        获取基础配置数据
        :param sector:
        :param item:
        :return:
        """
        value = None
        try:
            value = cls.__config_dic[sector][item]
        except KeyError:
            try:
                cf = configparser.ConfigParser()
                if cls.__path is None:
                    cls.__path = os.path.abspath(os.path.join(cls.__pro_path, "./config.conf"))
                cf.read(cls.__path, encoding='utf8')
                value = cf.get(sector, item)
                cls.__config_dic[sector][item] = value
            except KeyError:
                return None
        finally:
            return value

    @classmethod
    def get_str(cls, model, key):
        """
        获取string类型值
        :param model:
        :param key:
        :return:
        """
        _ret = cls.__get_config(model, key)
        if _ret:
            return _ret
        else:
            return ""

    @classmethod
    def get_bool(cls, model, key):
        """
        获取bool类型值
        :param model:
        :param key:
        :return:
        """
        _ret = cls.__get_config(model, key)
        return True if _ret and _ret.lower() in ['true', '1', 'yes'] else False

    @classmethod
    def get_dict(cls, model, key):
        """
        获取字典类型值
        :param model:
        :param key:
        :return:
        """
        _ret = cls.__get_config(model, key)
        if _ret:
            try:
                _ret = eval(_ret)
                return _ret
            except KeyError:
                return {}
        return {}

    @classmethod
    def get_int(cls, model, key):
        """
        获取int类型的值
        :param model:
        :param key:
        :return:
        """
        _ret = cls.__get_config(model, key)
        if _ret is not None:
            try:
                _ret = int(_ret)
                return _ret
            except KeyError:
                return 0
        return 0

    @classmethod
    def get_list(cls, model, key):
        """
        获取列表类型的值
        :param model:
        :param key:
        :return:
        """
        _ret = cls.__get_config(model, key)
        if _ret:
            try:
                _ret = eval(_ret)
                return _ret
            except KeyError:
                return []
        return []

    @classmethod
    def get_float(cls, model, key):
        """
        获取浮点类型的数据
        :param model:
        :param key:
        :return:
        """
        _ret = cls.__get_config(model, key)
        if _ret:
            try:
                _ret = eval(_ret)
                return _ret
            except KeyError:
                return 0
        return 0