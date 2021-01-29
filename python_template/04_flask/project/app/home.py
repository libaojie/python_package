
from flask import request, Response, json
from lbj_flask.enum.error_code import ErrorCode
from lbj_flask.res.comm_res import CommRes

from project.app import app


@app.route('/hi')
def hi():
    """
    心跳
    :return:
    """
    from lbj_flask.response_tool import ResponseTool
    from lbj_common.config_tool import ConfigTool
    from lbj_flask.ip_tool import IpTool

    data = {'version': ConfigTool.get_str('version', 'VERSION'), 'ipClient': IpTool.get_ip(request),  'ipServer': IpTool.get_local_ip(),  'port': ConfigTool.get_str('app', 'PORT'), 'isAuth': ConfigTool.get_str('ca', 'IS_AUTH')}
    return ResponseTool.get_json_ret(CommRes(ErrorCode.SUCCESS, data=data))


@app.route('/db')
def db():
    """
    心跳
    :return:
    """
    from lbj_flask.response_tool import ResponseTool
    from lbj_common.log_tool import LogTool
    from lbj_db.db_engine_tool import DBEngineTool
    from lbj_common.config_tool import ConfigTool

    data = {'dbUrl': ConfigTool.get_str('flask', 'SQL_CONN')}

    LogTool.info("测试数据库")
    _sql = """
    select * from dual
    """

    _ret = DBEngineTool.get_by_sql(_sql)
    if _ret is None:
        LogTool.error("数据库不通")
        data['dbConn'] = 'False'
    else:
        LogTool.info("数据库连通")
        data['dbConn'] = 'True'
    return ResponseTool.get_json_ret(CommRes(ErrorCode.SUCCESS, data=data))


@app.route('/health')
def health():
    """
    心跳
    :return:
    """
    t = {'status': 'UP'}
    return Response(json.dumps(t), mimetype='application/json')