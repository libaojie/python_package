#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/9/27 10:03
@Author     : libaojie
@File       : word_tool.py
@Software   : PyCharm
"""
from docxtpl import DocxTemplate

from lbj_common.decorator import except_fun
from lbj_common.file_tool import FileTool
from lbj_common.log_tool import LogTool


class WordTool(object):
    """
    word工具
    """

    @classmethod
    @except_fun
    def write_temp(cls, templatepath, filepath, context):
        """
        往模板中写数
        :param templatepath:
        :param filepath:
        :param context:
        :return:
        """
        if not FileTool.is_file(templatepath):
            LogTool.error(f"word模板不存在！{templatepath}")
            return None

        doc = DocxTemplate(templatepath)
        # context = {
        #     'col_labels':['水果', 'v1', 'v2', 'v3', 'v4'],
        #     'tbl_contents':[
        #         {'label':'yellow', 'cols':['11', '12', '13', '14', '15']},
        #         {'label':'green', 'cols':['21', '22', '23', '24', '25']}]
        # }
        doc.render(context)
        FileTool.mkdir_file(filepath)
        doc.save(filepath)

