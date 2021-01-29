#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/4/9 17:36
@Author     : libaojie
@File       : orm_tool.py
@Software   : PyCharm
"""
from lhzl_common.log_tool import LogTool
from lhzl_db.db_engine_tool import DBEngineTool
from lhzl_db.entity.ret_find import RetFind
from sqlalchemy import text

from lhzl_flask.enum.del_flag import DelFlag


class OrmTool(object):
    """
    ORM相关工具
    """

    @staticmethod
    def find_by_query(model, page_num=None, page_size=None, del_flag=DelFlag.view.value, precise_dict=None,
                      fuzzy_dict=None, other_str=None):
        """
        按条件查询
        :param model:
        :param page_num:
        :param page_size:
        :param del_flag:
        :param precise_dict:
        :param fuzzy_dict:
        :param other_str:
        :return: RetFind
        """
        query = model.query
        # 排序
        query = query.order_by(model.update_time.desc())
        # 数据状态
        if del_flag != DelFlag.all.value:
            query = query.filter(text(f"del_flag = '{del_flag}'"))
        # 精准查询字段
        if precise_dict and isinstance(precise_dict, dict) and len(precise_dict) > 0:
            for key, value in precise_dict.items():
                if not hasattr(model, key):
                    LogTool.error(f"【{model.__tablename__}】表找不到{key}字段")
                    continue
                if value:
                    query = query.filter(text(f"{key} = '{value}'"))

        # 模糊查询
        if fuzzy_dict and isinstance(fuzzy_dict, dict) and len(fuzzy_dict) > 0:
            for key, value in fuzzy_dict.items():
                if not hasattr(model, key):
                    LogTool.error(f"【{model.__tablename__}】表找不到{key}字段")
                    continue
                if value:
                    query = query.filter(text(f"regexp_like({key}, '{value}', 'i') "))

        # 其他过滤条件
        if other_str and isinstance(other_str, str):
            query = query.filter(text(f" {other_str} "))

        retFind = RetFind()
        if page_num:
            page_num, page_size = DBEngineTool.get_page_val(page_num, page_size)
            query = query.paginate(page_num, page_size, error_out=False)
            retFind.data = query.items
            retFind.page_num = page_num
            retFind.page_size = page_size
            retFind.page_total = query.pages
            retFind.total = query.total
        else:
            retFind.data = query.all()
            retFind.page_num = None
            retFind.page_size = None
            retFind.page_total = None
            retFind.total = None
        return retFind
