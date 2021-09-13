
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 测试For
@Time       : 2018/5/17 9:50
@Author     : libaojie
@File       : for_data.py
@Software   : PyCharm
"""

class ForData(object):

    def __init__(self):
        pass

    def for_if(self):
        print([x for x in range(10)])
        print([x if x % 2 == 0 else 1 for x in range(10)])
        print([x for x in range(10) if x % 2 == 0])
