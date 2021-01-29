#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 数据库链接基类
@Time       : 2020/02/06 20:05
@Author     : libaojie
@File       : db_base_tool.py
@Software   : PyCharm
"""
from lhzl_common.log_tool import LogTool
from lhzl_common.type_tool import TypeTool

from lhzl_db.entity.ret_find import RetFind
from lhzl_db.sql_tool import SQLTool


class DBBaseTool(object):
    """
    数据库操作基类
    """
    db = None  # 数据库链接
    db_session = None  # 数据库链接
    db_engine = None  # 数据库链接
    page_num = 1  # 默认页码
    page_size = 15  # 默认每页数量
    page_code = 'PAGE_ROW_CNT'  # 默认页码的数据库字典code
    page_key = 'DEFAULT'  # 默认每页数量数据字典key
    dict_tbl_name = 'lhzlmr.mr_dict'  # 数据字典表名

    def __init__(self):
        pass

    @classmethod
    def _get_db(cls):
        return cls.db

    @classmethod
    def init_db(cls, db):
        try:
            # 此处无需处理编译错误，lhzl-flask包会自动引用处理。
            from flask_sqlalchemy import SQLAlchemy
            if isinstance(db, SQLAlchemy):
                cls.db = db
                cls.db_session = db.session
                cls.db_engine = db.engine
                return
        except Exception as e:
            LogTool.info(f"db初始化失败：{str(e)}")

        try:
            from sqlalchemy.orm import Scoped_session
            if isinstance(db, Scoped_session):
                cls.db_session = db
                return
        except Exception as e:
            LogTool.info(f"session初始化失败：{str(e)}")

        try:
            from sqlalchemy.engine import Engine
            if isinstance(db, Engine):
                cls.db_engine = db
                return
        except Exception as e:
            LogTool.info(f"session初始化失败：{str(e)}")

        LogTool.error(f"初始化数据库连接失败！")

    @classmethod
    def init_page(cls, page_num, page_size, page_code, page_key, dict_tbl_name):
        """
        初始化分页参数
        :param page_numb:
        :param page_size:
        :param page_code:
        :param page_key:
        :param dict_tbl_name:
        :return:
        """
        cls.page_num = TypeTool.change_to_int(page_num)
        cls.page_size = TypeTool.change_to_int(page_size)
        cls.page_code = page_code
        cls.page_key = page_key
        cls.dict_tbl_name = dict_tbl_name

    @classmethod
    def run_sql(cls, sql):
        """
        运行sql
        :param sql:
        :return: RetRunSql
        """
        pass

    @classmethod
    def _find_dict_by_sql(cls, sql):
        """
        执行sql
        :param sql:
        :return:
        """
        ret_run_sql = cls.run_sql(sql)
        if ret_run_sql is not None and ret_run_sql.is_success:
            ret = []
            if ret_run_sql.val_list is not None and isinstance(ret_run_sql.val_list, list):
                for row in ret_run_sql.val_list:
                    ret.append(dict(zip(ret_run_sql.col_list, row)))
            return ret
        return None

    pass

    @classmethod
    def get_by_sql(cls, sql):
        """
        找到一条
        :param sql: str
        :return: Dict
        """
        ret = cls._find_dict_by_sql(sql)
        LogTool.info(f"执行get_sql结束,开始处理结果：{ret}")
        if ret is None:
            return None

        if ret:
            if ret and len(ret) > 0:
                return ret[0]
            else:
                return {}
        return None

    @classmethod
    def find_by_sql(cls, sql, page_num=None, page_size=None):
        """
        找到多条
        :param sql:
        :param page_num:
        :param page_size:
        :return RetFind:
        """
        ret_find_sql = RetFind()
        data = None
        total = None
        LogTool.info(f"开始执行翻页sql")
        if page_num:
            page_num, page_size = cls.get_page_val(page_num, page_size)

            next_page = page_num * page_size
            cur_page = (page_num - 1) * page_size + 1
            if page_num == 1 or cur_page < 0:
                cur_page = 0
                next_page = page_size

            run_sql = f"""
                              SELECT * FROM(
                              SELECT ROWNUM RN,T.* FROM({sql})T 
                              WHERE ROWNUM<={next_page}
                              )WHERE RN >={cur_page} 
                          """
        else:
            run_sql = sql

        ret = cls._find_dict_by_sql(run_sql)
        LogTool.info(f"执行翻页sql结束,开始处理结果：{ret}")
        if ret:
            if page_num and page_size:
                LogTool.info("获取总数")
                total = 0
                sum_sql = f"select count(*) total from ({sql})"
                sum_ret = cls._find_dict_by_sql(sum_sql)
                LogTool.info(f"总数查询结果：{sum_ret}")
                if sum_ret and len(sum_ret) > 0:
                    if sum_ret[0].__contains__('TOTAL'):
                        total = sum_ret[0]['TOTAL']
                    elif sum_ret[0].__contains__('total'):
                        total = sum_ret[0]['total']
                data = []
                for r in ret:
                    if r.__contains__('rn'):
                        del r["rn"]
                    if r.__contains__('RN'):
                        del r["RN"]
                    data.append(r)
            else:
                data = ret

        # TODO 李宝杰  需处理返回结构
        ret_find_sql.page_num = page_num
        ret_find_sql.page_size = page_size
        ret_find_sql.page_total = None
        ret_find_sql.total = total if total else 0
        ret_find_sql.data = data
        return ret_find_sql
        # from project.app.plugins.response_tool import ResponseTool
        # return ResponseTool.return_page(data, total, page, page_size)

    @classmethod
    def get_page_val(cls, page_num, page_size):
        """
        获取值
        :param page:
        :param page_size:
        :return:
        """
        if page_num:
            page_num = TypeTool.change_to_int(page_num)
            if page_num is None:
                page_num = cls.page_num

            if page_size is None:
                _dict_sql = f"select dict_val from {cls.dict_tbl_name} where dict_code = '{cls.page_code}' and dict_key = '{cls.page_key}'"
                _dict_ret = cls.get_by_sql(_dict_sql)
                if _dict_ret is None or not _dict_ret.__contains__('dict_val'):
                    LogTool.error(f"找不到分页数据字典项：{cls.dict_tbl_name} {cls.page_code} {cls.page_size}")
                else:
                    page_size = _dict_ret['dict_val']

            page_size = TypeTool.change_to_int(page_size)
            if page_size is None:
                page_size = cls.page_size
        else:
            page_size = None

        return page_num, page_size

    @classmethod
    def clear_tbl_data(cls, tbl_name):
        """
        清空表数据
        :param tbl_name:
        :return:
        """
        sql = SQLTool.get_truncate_sql(tbl_name)
        ret_run_sql = cls.run_sql(sql)
        if not ret_run_sql and ret_run_sql.is_success:
            # 失败
            sql = SQLTool.get_delete_sql(tbl_name)
            ret_run_sql = cls.run_sql(sql)
            if not ret_run_sql and ret_run_sql.is_success:
                # 失败
                LogTool.error(f'无法清表{tbl_name}')
                return False
        return True
