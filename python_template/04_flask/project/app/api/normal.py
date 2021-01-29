#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/8/9 10:21
@Author     : libaojie
@File       : init_db.py
@Software   : PyCharm
"""

from flask import request
from lbj_common.decorator import except_fun
from lbj_flask.enum.error_code import ErrorCode
from lbj_flask.request_tool import RequestTool
from lbj_flask.res.comm_res import CommRes
from lbj_flask.response_tool import ResponseTool

from project.app import blueprint_authority


@except_fun
@blueprint_authority.route("/normal", methods=["GET"])
def get():
    page, per_page = RequestTool.get_request_page(request)
    id = request.args.get('id')
    return ResponseTool.get_json_ret(CommRes(ErrorCode.SUCCESS))


@blueprint_authority.route("/normal", methods=["POST"])
def post():
    f = request.files['file']
    data = request.form['user']
    code = request.json.get('code')

    return ResponseTool.get_json_ret(CommRes(ErrorCode.SUCCESS))
