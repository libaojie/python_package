#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/8/16 10:39
@Author     : libaojie
@File       : engine.py
@Software   : PyCharm
"""
import threading


class Engine(object):
    """
    单例引擎
    """

    __instance = None  # 定义一个类属性做判断
    __instance_lock = threading.Lock()
    _t = 0

    def __new__(cls):
        if cls.__instance is None:
            # 如果__instance为空证明是第一次创建实例
            # 通过父类的__new__(cls)创建实例
            with cls.__instance_lock:
                cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            # 返回上一个对象的引用
            return cls.__instance

    @classmethod
    def init(cls, type, param):
        """
        初始化
        :param handle_id:
        :return:
        """
        pass
