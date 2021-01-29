#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/8/16 14:43
@Author     : libaojie
@File       : df_tool.py
@Software   : PyCharm
"""
import pandas as pd
from lbj_common.log_tool import LogTool


class DFTool(object):

    @staticmethod
    def df_is_null(df):
        """
        验证是否为空
        :param df:
        :return:
        """
        return df is None or df.empty

    @staticmethod
    def df_append(df_list):
        """
        DataFrame合并
        :param df_list:
        :return:
        """

        if len(df_list) == 0:
            return None

        df = None
        for index, value in enumerate(df_list):
            if index < 1:
                df = value
            else:
                if DFTool.df_is_null(df):
                    df = value
                elif not DFTool.df_is_null(value):
                    df = df.append(value, sort=True)
        return df

    @staticmethod
    def df_concat(df_list):
        """
        DataFrame合并
        :param self:
        :param df1:
        :param df2:
        :return:
        """
        if len(df_list) == 0:
            return None
        return pd.concat(df_list, sort=True)

    @staticmethod
    def df_drop(df, colums):
        """
        DataFrame 删除列
        :param df:
        :param colums:
        :return:
        """
        if df is None or df.empty:
            return df

        colums = [col for col in colums if col in df.columns.tolist()]
        df = df.drop(colums, axis=1)
        return df

    @staticmethod
    def df_drop_duplicate(df, colums):
        """
        DataFrame 去空
        :param df:
        :param colums:
        :return:
        """
        if df is None or df.empty:
            return df

        colums = [col for col in colums if col in df.columns.tolist()]
        df = df.drop_duplicates(colums)
        return df

    @staticmethod
    def df_print(name, df):
        LogTool.print(f"标记{name} 长度：{df.shape}  列名：{df.columns.values.tolist()}")

    @staticmethod
    def df_merge(df1, df2, how='inner', on=None):
        """
        DataFrame 交集
        :param DataFrame df1:
        :param DataFrame df2:
        :param list columns:
        :return:
        """
        if df1 is None:
            return df2 if how == 'right' else None

        if df2 is None:
            return df1 if how == 'left' else None

        _inner = pd.merge(df1, df2, how=how, on=on)
        _inner = _inner.drop_duplicates()
        return _inner

    @staticmethod
    def df_diff(df1, df2, columns=None):
        """
        DataFrame 差集
        :param DataFrame df1:
        :param DataFrame df2: df2是df1的子集
        :param list columns:
        :return:
        """
        _diff = DFTool.df_append([df1, df2])
        _diff = DFTool.df_append([_diff, df2])
        df = _diff.drop_duplicates(subset=columns, keep=False)
        return df

    @staticmethod
    def df_rename(df, columns):
        """
        重命名
        :param df:
        :param columns:
        :return:
        """
        if df is None:
            return None
        df = df.rename(columns=columns)
        return df

    @staticmethod
    def df_split(df, conditions):
        """
        传入条件拆分为两个DataFrame
        第一个为True
        第二个为False
        :param df:
        :param conditions:
        :return:
        """
        df_true = None
        df_false = None
        if df is None or df.empty:
            return df_true, df_false

        df_list = df.groupby(conditions)
        for d in df_list:
            if d[0]:
                df_true = d[1]
            else:
                df_false = d[1]
        return df_true, df_false

    @staticmethod
    def get_map_value(df, value, key_col, ret_col):
        """
        针对数据映射关系，通过实际值获取映射后的标准值
        :param df:
        :param value: 值
        :param key_col:
        :param ret_col:
        :return:
        """
        _s = df[df[key_col] == value]  # 获取对应的数据行，允许多行

        if _s.shape[0] > 0:
            _ret = _s[ret_col].iloc[0]  # 获取标准化后的值，如果多行数据的时候，选择首行
        else:
            # 未标准化
            _ret = None
        return _ret

    @staticmethod
    def check_df_col_null(df, check_col, ret_col, error_key):
        """
        检查空值
        :param df:
        :param check_col:
        :param ret_col:
        :param error_key:
        :return:
        """
        def _f_add_error(x):
            if isinstance(ret_col, str):
                info = [x[ret_col]]
            elif isinstance(ret_col, list):
                info = [None if i is None else x[i] for i in ret_col]

            # LogTool.error('标准化问题；{0} 信息；{1}'.format(error_key, info))

        if df is not None and not df.empty:
            df[pd.isnull(df[check_col])].apply(_f_add_error, axis=1)
