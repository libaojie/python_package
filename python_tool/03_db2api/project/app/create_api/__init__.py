#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    :
@Time       : 2019/9/23 10:51
@Author     : libaojie
@File       : __init__.py.py
@Software   : PyCharm
"""
import os

from flask import Blueprint, render_template, request, make_response, send_file
from lbj_common.config_tool import ConfigTool
from lbj_common.decorator import except_fun
from lbj_common.log_tool import LogTool
from lbj_common.style_tool import StyleTool
from lbj_common.utils import Utils
from lbj_db.sql_tool import SQLTool
from lbj_flask.response_tool import ResponseTool
from lbj_word.word_tool import WordTool

from project.app.plugins.db_engine_src_tool import DBEngineSrcTool
from project.app.plugins.engine_tool import EngineTool

blueprint_create = Blueprint("blueprint_create", __name__, url_prefix='/tool/createApi')


@blueprint_create.route("/index", methods=["GET"])
def index():
    db = request.args.get('db')
    tblName = request.args.get('tblName')
    cols = []
    if db is not None and tblName is not None:
        sql = """
        select 
            a.Table_name as "tblName",
            a.column_name as "colName",
            a.data_type as "colType",
            a.data_length as "colLen",
            a.data_precision as "dataPre",
            a.nullable as "isNull",
            a.column_id as "colId",
            b.comments as "remark"
        from user_tab_columns a 
        left join user_col_comments b on a.TABLE_NAME=b.table_name and a.COLUMN_NAME=b.column_name 
        where

        """
        sql = SQLTool.get_tmpl_sql(sql, precise_dict={'a.Table_name': tblName.upper()})
        db_engine = EngineTool.get_engine(db)
        cols = DBEngineSrcTool.find_dict_by_sql(sql, db_engine)

        pass

    return render_template('create_api/index.html', cols=cols)


@blueprint_create.route("/getCols", methods=["GET"])
def getCols():
    db = request.args.get('db')
    tblName = request.args.get('tblName')
    cols = []
    if db is not None and tblName is not None:
        sql = """
        select 
            a.Table_name as "tblName",
            a.column_name as "colName",
            a.data_type as "colType",
            a.data_length as "colLen",
            a.data_precision as "dataPre",
            a.nullable as "isNull",
            a.column_id as "colId",
            b.comments as "remark"
        from user_tab_columns a 
        left join user_col_comments b on a.TABLE_NAME=b.table_name and a.COLUMN_NAME=b.column_name 
        where

        """
        sql = SQLTool.get_tmpl_sql(sql, precise_dict={'a.Table_name': tblName.upper()})
        db_engine = EngineTool.get_engine(db)
        cols = DBEngineSrcTool.find_dict_by_sql(sql, db_engine)

        if cols is not None:
            for col in cols:
                col['newColName'] = StyleTool.first_lower(StyleTool._2Upper(col['colName']))

        pass

    return render_template('create_api/index_col.html', cols=cols)


@blueprint_create.route("/handleCols", methods=["POST"])
def handleCols():
    return _handleCols()


@except_fun
def _handleCols():
    db = request.form.get('db')
    tblName = request.form.get('tblName')
    url = request.form.get('url')
    serv = request.form.get('serv')
    type = request.form.get('type')
    isChecked = request.form.getlist("isChecked")
    colName = request.form.getlist("colName")
    isNull = request.form.getlist("isNull")
    value = request.form.getlist("colValue")
    remark = request.form.getlist("remark")

    # 处理参数
    size = int(len(isChecked) / 2)
    req_is_checked = isChecked[:size]
    rep_is_checked = isChecked[size:]
    req_colName = colName[:size]
    rep_colName = colName[size:]
    req_is_null = isNull[:size]
    rep_is_null = isNull[size:]
    req_value = value[:size]
    rep_value = value[size:]
    req_remark = remark[:size]
    rep_remark = remark[size:]

    reqs = []
    reps = []
    req_index = 0
    rep_index = 0
    for i in range(size):
        if req_is_checked[i] == '1':
            req_index = req_index + 1
            req = {'index': req_index}
            if len(req_colName) > i:
                req['colKey'] = req_colName[i]
            if len(req_value) > i:
                req['value'] = req_value[i]
            if len(req_is_null) > i:
                req['isNull'] = req_is_null[i]
            if len(req_remark) > i:
                req['remark'] = req_remark[i]
            reqs.append(req)
        if rep_is_checked[i] == '1':
            rep_index = rep_index + 1
            rep = {'index': rep_index}
            if len(rep_colName) > i:
                rep['colKey'] = rep_colName[i]
            if len(rep_value) > i:
                rep['value'] = rep_value[i]
            if len(rep_is_null) > i:
                rep['isNull'] = rep_is_null[i]
            if len(rep_remark) > i:
                rep['remark'] = rep_remark[i]
            reps.append(rep)

    context = {
        "serv": serv,
        "type": type,
        "url": url,
        "reqs": reqs,
        "reps": reps
    }
    uuid = Utils.get_uuid()
    temp_path = os.path.join(ConfigTool.get_path(), rf"doc/create_api/temp_{type.lower()}.docx")
    LogTool.info(f"模板地址：{temp_path}")
    if os.path.exists(temp_path):
        file_name = f"{type.lower()}.docx"
        file_path = os.path.join(ConfigTool.get_path(), r"data/temp", uuid)
        out_path = os.path.join(file_path, file_name)
        LogTool.info(f"输出路径：{out_path}")
        WordTool.write_temp(temp_path, out_path, context)
        if os.path.isfile(out_path):
            # 存在文件
            return ResponseTool.get_json_ret(data={"url": out_path, "fileName": file_name})
            # response = make_response(send_file(out_path))
            # response = make_response(send_from_directory(file_path, file_name, as_attachment=True))
            # response.headers["Content-Disposition"] = "attachment; filename={}".format(
            #     file_name.encode().decode('latin-1'))
            # return response
    return None


@blueprint_create.route("/download", methods=["GET"])
def download():
    path = request.args.get('path')
    LogTool.info(f"下载路径{path}")
    if os.path.isfile(path):
        # 存在文件
        LogTool.info(f"存在")
        response = make_response(send_file(path))
        return response