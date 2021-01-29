#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : sql拼接模版
@Time       : 2019/8/16 14:55
@Author     : libaojie
@File       : sql_tool.py
@Software   : PyCharm
"""
import datetime

from lbj_common.log_tool import LogTool
from lbj_common.time_tool import TimeTool


class SQLTool(object):
    """
    SQL拼接模版
    """

    @staticmethod
    def get_select_sql(table_name, columns=None, precise_dict=None, fuzzy_dict=None, other_str=None):
        """
        组织搜索语句
        :param table_name:
        :param columns:
        :param precise_list: 精准
        :param fuzzy_list: 模糊
        :param other_list: 其他
        :return:
        """

        # 条件
        condition_list = ['1=1']

        # 精准查询字段
        if precise_dict and isinstance(precise_dict, dict) and len(precise_dict) > 0:
            for key, value in precise_dict.items():
                if value is not None:
                    condition_list.append(f" {key} = '{value}' ")

        # 模糊查询
        if fuzzy_dict and isinstance(fuzzy_dict, dict) and len(fuzzy_dict) > 0:
            for key, value in fuzzy_dict.items():
                if value is not None:
                    condition_list.append(f" {key} like '%{value}%' ")

        con_str = " and ".join(condition_list)
        # 其他条件
        if other_str is not None:
            con_str = f" {con_str} {other_str}"

        # 列名
        _col_str = '*'
        if columns is not None and len(columns) > 0:
            _col_str = ','.join(columns)

        _sql = 'select {0} from {1} where {2}'.format(_col_str, table_name, con_str)
        return _sql

    @staticmethod
    def get_tmpl_sql(tepl, precise_dict=None, fuzzy_dict=None, other_str=None):
        """
        组织模板sql语句
        :param table_name:
        :param columns:
        :param precise_dict:
        :param fuzzy_dict:
        :param other_list:
        :return:
        """
        if tepl is None:
            LogTool.error(f"传入的sql模板不合法：{tepl}")
            return None

        # 条件
        condition_list = ['1=1']
        # 精准查询字段
        if precise_dict and isinstance(precise_dict, dict) and len(precise_dict) > 0:
            for key, value in precise_dict.items():
                if value is not None:
                    condition_list.append(f" {key} = '{value}' ")

        # 模糊查询
        if fuzzy_dict and isinstance(fuzzy_dict, dict) and len(fuzzy_dict) > 0:
            for key, value in fuzzy_dict.items():
                if value is not None:
                    condition_list.append(f" {key} like '%{value}%' ")

        # 其他条件
        con_str = " and ".join(condition_list)
        if other_str is not None:
            con_str = f" {con_str} {other_str}"

        return f"{tepl} {con_str}"

    @staticmethod
    def get_update_sql(tbl_name, df, keys, ignore_col=None):
        """
        组织多条记录更新数据库
        :param ptbl_name:
        :param pcols:
        :return:
        """
        # 拼接关键字
        _key = None
        for key in keys:
            if _key is None:
                _key = key
            else:
                _key = 'CONCAT(CONCAT({0},\',\'), {1})'.format(_key, key)

        # 生成所有关键字的值
        df['key'] = df.apply(lambda x: '\'{0}\''.format(','.join([str(x[key]) for key in keys])), axis=1)

        # 关键字的值 的列表
        _key_values = list(df['key'])

        ignore_key = ['key'] + keys if ignore_col is None else ['key'] + keys + ignore_col
        _value_list = []
        for col in df.columns:
            if not col in ignore_key:
                _when_list = []

                def _get_when(x):
                    _str = 'when {0}={1} then \'{2}\''.format(_key, x['key'], x[col])
                    _when_list.append(_str)
                    pass

                df.apply(_get_when, axis=1)

                _item = '{0} = case {1} end'.format(col, ' '.join(_when_list))
                _value_list.append(_item)

        df.drop(['key'], axis=1, inplace=True)

        _value = ','.join(_value_list)

        # IN 查询时出现ORA-01795:列表中的最大表达式数为1000
        size = 1000
        _key_size = []
        for i in range(len(_key_values)):
            if len(_key_size) == 0:
                # 第一个元素直接创建
                _key_size.append([_key_values[i]])
            elif len(_key_size[len(_key_size) - 1]) < size:
                # 最后元素长度未超过
                _key_size[len(_key_size) - 1].append(_key_values[i])
            else:
                # 超过了添加新的
                _key_size.append([_key_values[i]])

        _in = ['{0} in ({1})'.format(_key, ','.join(_k_z)) for _k_z in _key_size]
        _condition = ' or '.join(_in)

        return 'update {0} set {1} where {2}'.format(tbl_name, _value, _condition)

    @staticmethod
    def get_insert_sql(tbl_name, col_name, value):
        """
        获取多条记录插入数据库
        :param tbl_name:
        :param col_name:
        :param value:
        :return:
        """
        if col_name is None or not isinstance(col_name, list) or len(col_name) < 1:
            return None
        if tbl_name is None:
            return None
        if value is None or not isinstance(value, list) or len(value) < 1:
            return None

        col_str = ','.join(col_name)
        rows = []
        for row in value:
            if row is not None and isinstance(row, list) and len(row) > 0 and len(row) == len(col_name):
                # row_str = ['null' if val is None else f"'{val}'" for val in row]
                # row_str = ['null' if val is None else val for val in row]
                t_row = []
                for val in row:
                    if val is None:
                        t_row.append('null')
                    elif isinstance(val, int):
                        t_row.append(f'{val}')
                    elif isinstance(val, datetime.datetime):
                        t_row.append(TimeTool.get_sql_str(val))
                    else:
                        if "'" in val:
                            val = val.replace("'", "''")
                        t_row.append(f"'{val}'")

                rows.append(f"into {tbl_name}({col_str}) values ({','.join(t_row)})")

        if len(rows) < 1:
            return None

        return f"""
        insert all
        {' '.join(rows)}
        select 1 from dual
        """

    @staticmethod
    def get_insert_tmpl_sql(ptbl_name, pcols):
        """
        组织插入语句的模板
        :param ptbl_name: String 数据库表名
        :param pcols: List 数据列名组成的列表
        :return:
        """
        _item = [':{0}']  # 定义展位符元素
        _items = _item * len(pcols)  # 定义最终的占位符列表
        for i in range(len(_items)):
            _items[i] = _items[i].format(i + 1)

        _items_str = ','.join(_items)  # 获取列字符串
        _cols_str = ','.join(pcols)  # 获取占位符字符串

        # 指定Insert语句的模板
        _insert_sql_fomat = """INSERT INTO {tbl_name} ({cols}) VALUES ({items})"""

        # 返回Insert语句
        return _insert_sql_fomat.format(tbl_name=ptbl_name,
                                        cols=_cols_str,
                                        items=_items_str)

    @staticmethod
    def get_delete_sql(ptbl_name):
        """
        得到删除语句
        :param ptbl_name:
        :return:
        """
        ptbl_name = ptbl_name.lower()
        return f"delete from {ptbl_name}"

    @staticmethod
    def get_truncate_sql(tbl_name):
        """

        :param tbl_name:
        :return:
        """
        tbl_name = tbl_name.lower()
        return f'truncate table {tbl_name}'