#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/4/9 10:55
@Author     : libaojie
@File       : df_db_tool.py
@Software   : PyCharm
"""
import pandas as pd
from lhzl_common.decorator import log_fun
from lhzl_common.df.df_tool import DFTool
from lhzl_common.log_tool import LogTool

from lhzl_db.db_engine_tool import DBEngineTool
from lhzl_db.sql_tool import SQLTool


class DFDBTool(object):

    @classmethod
    @log_fun
    def df_from_db(cls, table_name, columns=None, precise_dict=None, fuzzy_dict=None, other_str=None):
        """
        数据库中获取表数据
        :param table_name:
        :param columns:
        :param precise_dict:  精准查询条件
        :param fuzzy_dict:  模糊查询条件
        :param other_str:  其他条件
        :return:
        """
        # 小写转化
        table_name = table_name.lower()
        LogTool.info(f"表名：【{table_name}】")
        if columns is not None:
            columns = [col.lower() for col in columns]

        _sql = SQLTool.get_select_sql(table_name, columns, precise_dict, fuzzy_dict, other_str)
        return cls.get_df_by_sql(_sql)

    @classmethod
    @log_fun
    def df_to_db(cls, table_name, df, keys=None, ignore_col=None):
        """
        DataFrame写入数据库
        :param table_name:
        :param df:
        :param keys:
        :param ignore_col:
        :return:
        """
        LogTool.info(f"表名：【{table_name}】")
        if df.empty:
            return True

        df = df.fillna('')
        df = df.replace(['None', 'none', 'nan', 'NAN'], '')
        df = cls.after_df_null(df)

        def _f_change_special(x):
            """
            处理每项数据中的特殊值
            :param x:
            :return:
            """
            if isinstance(x, str):
                x = x.replace('\'', '\'\'')
                # if constant.IS_ORACLE:
                # x = x.replace('\'', '\'\'')
                # 处理oracle编码问题
                # x = x.encode('GBK', 'ignore').decode('GBK')
                # else:
                # x = x.replace('\\', '\\\\')
                # x = x.replace('\'', '\\\'')
            return x

        df = df.applymap(_f_change_special)

        return cls._save_by_df(table_name, df, keys=keys, ignore_col=ignore_col)

    @classmethod
    def _save_by_df(cls, table_name, df, keys=None, ignore_col=None):
        """
        DataFrame 入库 有则更新 无则追加
        :param table_name: str 数据库表名
        :param df: DataFrame 数据结构
        :param keys: list 更新时，主键   如果传None为纯插入
        :param ignore_col: list 忽略更新的字段
        :param back_col: list 有更新时，将数据库值更新回df的字段
        :return:
        """
        table_name = table_name.lower()
        if keys is not None:
            # 有主键才更新
            _used_col = df.columns.tolist() if ignore_col is None else [_c for _c in df.columns.tolist() if
                                                                        _c not in ignore_col]

            db_data = cls.get_df_by_sql(SQLTool.get_select_sql(table_name, _used_col))

            if db_data is not None and not db_data.empty:
                db_data = db_data.fillna('')
                # 原始数据与数据库数据交集
                _inner = DFTool.df_merge(df, db_data[keys], on=keys)

                # 交集与数据库中不一致的数据， 即需要更新的数据
                _inner_inner = DFTool.df_merge(_inner, db_data, on=_used_col)
                _inner_diff = DFTool.df_diff(_inner, _inner_inner, _used_col)

                if not cls.update_by_df(table_name, _inner_diff, keys, ignore_col=ignore_col):
                    return False

                # 差集
                df = DFTool.df_diff(df, _inner, keys)
                if df.empty:
                    # 更新完毕，无插入项
                    return True

        if not cls.insert_by_db(table_name, df):
            return False

        return True

    @classmethod
    def get_df_by_tbl(cls, tbl_name):
        sql = SQLTool.get_select_sql(tbl_name)
        return cls.get_df_by_sql(sql)

    @classmethod
    def get_df_by_sql(cls, sql, is_lower=True):
        """
        通过sql语句获取dataframe
        :param sql:
        :return:
        """

        # 优化后性能要高！！！
        retRunSql = DBEngineTool.run_sql(sql)
        if (retRunSql is not None
                and retRunSql.is_success
                and retRunSql.col_list is not None
                and isinstance(retRunSql.col_list, list)
                and retRunSql.val_list is not None
                and isinstance(retRunSql.val_list, list)):
            return pd.DataFrame(list(retRunSql.val_list),
                                columns=[v.lower() for v in retRunSql.col_list] if is_lower else retRunSql.col_list)
        else:
            return None

    @classmethod
    def before_df_null(cls, df):
        """
        处理空
        :param df:
        :return:
        """
        # 暂时去掉去空
        # df = df.replace(['', 'None', 'nan'], None)
        return df

    @classmethod
    def after_df_null(cls, df):
        """
        处理空
        :param df:
        :return:
        """
        df = df.fillna('')
        df = df.replace(['None', 'none', 'nan', 'NAN'], '')
        return df

    @classmethod
    def update_by_df(cls, table_name, df, keys=None, ignore_col=None):
        """
        DataFrame直接更新数据库
        :param table_name:
        :param df:
        :param keys:
        :param ignore_col:
        :return:
        """
        if df.empty:
            return True

        update_sql = SQLTool.get_update_sql(table_name, df, keys, ignore_col=ignore_col)
        retRunSql = DBEngineTool.run_sql(update_sql)
        if retRunSql is None or not retRunSql.is_success:
            LogTool.error(f'更新【{table_name}】表失败！')
            return False
        return True

    @classmethod
    def insert_by_db(cls, table_name, df):
        """
        DataFrame直接入库
        :param table_name:
        :param df:
        :return:
        """
        LogTool.info(f'插入表名;【{table_name}】')
        if DFTool.df_is_null(df):
            LogTool.info(f'插入数据库为空;【{table_name}】')
            return False

        pcols = df.columns.tolist()
        prow_vals = df.values.tolist()
        insert_sql = SQLTool.get_insert_tmpl_sql(table_name, pcols)
        ret = DBEngineTool.executemany(insert_sql, prow_vals)
        if not ret:
            LogTool.error(f'插入【{table_name}】表失败！')
            LogTool.error(f'插入sql 为：【{insert_sql}】')
            return False

        return True
