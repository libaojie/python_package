#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/9/20 21:33
@Author     : libaojie
@File       : db_engine_src_tool.py
@Software   : PyCharm
"""
from lbj_common.log_tool import LogTool

from project.app.extensions import db


class DBEngineSrcTool(object):
    """
    连接方式为Engine
    """

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    @classmethod
    def run_sql(cls, sql, db_engine=None):
        """
        执行sql
        :param sql:
        :return:
        """
        sql = sql.replace('\n', '')
        key = None
        value = None
        if db_engine is None:
            db_engine = db.engine
        conn = db_engine.raw_connection()
        cursor = conn.cursor()  # 打开操作游标
        try:
            LogTool.info('执行sql：{0}'.format(sql))
            ret = cursor.execute(sql)  # 执行数据插入操作
            conn.commit()
            try:
                key = [r[0] for r in ret.description]
                value = ret.fetchall()
            except Exception as e:
                pass
            LogTool.info(f"执行sql结束")
            return True, key, value
        except Exception as e:
            conn.rollback()  # 异常则回滚
            LogTool.error("执行数据库报错，报错信息：{0}\n报错语句：{1}".format(e, sql))
            return False, None, None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def find_dict_by_sql(cls, sql, db_engine=None):
        """
        执行sql
        :param sql:
        :return:
        """
        flag, key, value = cls.run_sql(sql, db_engine=db_engine)
        if flag:
            ret = []
            if value is not None and isinstance(value, list):
                for row in value:
                    ret.append(dict(zip(key, row)))
            return ret
        return None
