#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 数据库Engine操作
@Time       : 2020/02/06 20:05
@Author     : libaojie
@File       : db_base_tool.py
@Software   : PyCharm
"""
from lbj_common.decorator import log_fun
from lbj_common.log_tool import LogTool

from lbj_db.db_base_tool import DBBaseTool
from lbj_db.entity.ret_run_sql import RetRunSql
from lbj_db.sql_tool import SQLTool


class DBEngineTool(DBBaseTool):
    """
    数据库Engine操作
    """

    def __init__(self):
        super().__init__()
        pass

    @classmethod
    def _get_engine(cls):
        # return create_engine(ConfigTool.get_str('flask', 'SQLALCHEMY_DATABASE_URI'))
        if cls.db_engine is None:
            LogTool.error(f"Engine初始化失败！")
        return cls.db_engine

    @classmethod
    @log_fun
    def run_sql(cls, sql):
        """
        执行sql
        :param sql:
        :return: RetRunSql
        """
        db_engine = cls._get_engine()
        if db_engine is None:
            return None

        sql = sql.replace('\n', '')
        retRunSql = RetRunSql()
        conn = db_engine.raw_connection()
        try:
            # LogTool.info('执行sql：{0}'.format(sql))
            cursor = conn.cursor()  # 打开操作游标
            ret = cursor.execute(sql)  # 执行数据插入操作
            try:
                if ret is None:
                    # 主要是update和delete语句
                    rowcount = cursor.rowcount  # 影响行数
                    if rowcount is not None and rowcount > 0:
                        retRunSql.is_success = True
                    else:
                        LogTool.error(f"执行sql一行未影响；【{sql}】")
                else:
                    # 主要是 select语句
                    retRunSql.col_list = [r[0] for r in ret.description]
                    retRunSql.val_list = ret.fetchall()
                    retRunSql.is_success = True
            except Exception as e:
                LogTool.error(f"执行sql解析结果【{str(e)}】；【{sql}】")
                pass
            conn.commit()
            cursor.close()
            # LogTool.info(f"执行sql结束")
            return retRunSql
        except Exception as e:
            conn.rollback()  # 异常则回滚
            LogTool.error(f"执行数据库报错：【{e}】")
            LogTool.error(f"sql：【{sql}】")
            return retRunSql
        finally:
            conn.close()

    @classmethod
    @log_fun
    def executemany(cls, sql, val):
        """
        批量插入
        :param sql: string
        :param val: list 二维数组
        :return: Bool 是否插入成功
        """
        db_engine = cls._get_engine()
        if db_engine is None:
            return None

        sql = sql.replace('\n', '')
        conn = db_engine.raw_connection()
        cursor = conn.cursor()  # 打开操作游标
        try:
            LogTool.info(f'插入数据量;【{len(val)}】')
            cursor.executemany(sql, val)  # 执行数据插入操作
            conn.commit()  # 正常则提交
            cursor.close()
            return True
        except Exception as e:
            conn.rollback()  # 异常则回滚
            LogTool.error(f"插入数据库报错：【{e}】")
            LogTool.error(f"sql：【{sql}】")
            LogTool.error(f"val：【{val}】")
            return False
        finally:
            conn.close()

    @classmethod
    @log_fun
    def insert_rows(cls, ptbl_name, pcols, prow_vals):
        """
        插入数据记录集，支持多条记录按List插入
        :param ptbl_name: String 数据库表名
        :param pcols: List 数据列名组成的列表，一个元素代表一列
        :param prow_vals: List 值列表，一个元素代表一行，一行内的元素个数要与SQL中的数量对应
        :return: Bool 是否插入成功
        """
        LogTool.info(f"列表数据入库：表名【{ptbl_name}】数据量【{len(pcols)}】")
        if len(pcols) == 0 or len(prow_vals) == 0:
            LogTool.error(f"数据参数错误：pcols【长度为{len(pcols)}】或prow_vals【长度为{len(prow_vals)}】异常")
            return False

        _insert_sql = SQLTool.get_insert_tmpl_sql(ptbl_name, pcols)

        return cls.executemany(_insert_sql, prow_vals)

    @classmethod
    @log_fun
    def find_count(cls, sql):
        """
        获取数量
        :param sql: 示例 'select count(id) from ca_application'
        :return:
        """
        ret = DBEngineTool.get_by_sql(sql)
        if ret:
            for v in ret.values():
                return 0 if v is None else v