import base64

from flask import request
from flask_restful import Resource
from lbj_common.decorator import except_fun
from lbj_common.log_tool import LogTool
from lbj_flask.enum.error_code import ErrorCode
from lbj_flask.request_tool import RequestTool
from lbj_flask.res.comm_res import CommRes
from lbj_flask.response_tool import ResponseTool

from project.app.model.restful_model import RestfulModel


class RestfulRes(Resource):
    """
    Restful风格
    """

    @except_fun
    def get(self):
        '''
        查询
        :return:
        '''
        page, per_page = RequestTool.get_request_page(request)

        id = request.args.get('id')
        LogTool.info(f'参数列表：(id:{id})')
        _ret = RestfulModel.find_by_orm(page, per_page, id)
        return ResponseTool.get_json_ret(_ret)

    def post(self):
        """
        新增
        :return:
        """
        id = request.json.get('id')  #

        restfulModel = RestfulModel(id)
        if not restfulModel.save():
            return ResponseTool.get_json_ret(CommRes(ErrorCode.INSERT_FAILURE))

        return ResponseTool.get_json_ret(CommRes(ErrorCode.SUCCESS))

    def delete(self):
        """
        删除
        :return:
        """
        ids = request.args.get('ids')  # 获取调度计划id
        return ResponseTool.get_json_ret(CommRes(ErrorCode.SUCCESS))

    def put(self):
        """
        修改
        :return:
        """
        id = request.json.get('id')  # 主键
        remark = request.json.get('remark')  # 备注
        restfulModel = RestfulModel.get_by_id(id)
        if not restfulModel:
            return ResponseTool.get_json_ret(CommRes(ErrorCode.NOT_FOUND, data={"id": id}))
        restfulModel.remark = remark

        if not restfulModel.update():
            return ResponseTool.get_json_ret(CommRes(ErrorCode.UPDATE_FAILURE, data={'id': id}))

        return ResponseTool.get_json_ret(CommRes(ErrorCode.SUCCESS))


class RestfulCollRes(Resource):
    """
    列表服务
    """

    def get(self):
        """
        获取所有列表
        :return:
        """
        page, per_page = RequestTool.get_request_page(request)

        id = request.args.get('id')
        _ret = RestfulModel.find_by_orm(page, per_page, id)
        return ResponseTool.get_json_ret(CommRes(ErrorCode.SUCCESS, data=_ret))
