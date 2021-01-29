#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 认证中心
@Time       : 2018/7/20 15:46
@Author     : libaojie
@File       : __init__.py
@Software   : PyCharm
"""
import os
import platform
import sys

from flask import Flask, Response, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


def __init_env():
    """
    初始化环境
    :return:
    """
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def __init_log():
    """
    初始化日志模块
    :return:
    """
    from lbj_common.config_tool import ConfigTool
    log_path = os.path.abspath(os.path.join(ConfigTool.get_path(), ConfigTool.get_str("logging", "path")))

    from lbj_common.log_tool import LogTool
    LogTool.init(log_path)
    LogTool.info("---------第一条日志----------")


def __init_app_config():
    """
    初始化配置
    :return:
    """
    from lbj_common.config_tool import ConfigTool
    from lbj_db.conn.flask_conn_tool import FlaskConnTool
    from lbj_common.log_tool import LogTool

    app.config['DEBUG'] = ConfigTool.get_bool('flask', 'DEBUG')
    app.config['JSON_AS_ASCII'] = ConfigTool.get_str('flask', 'JSON_AS_ASCII')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = ConfigTool.get_str('flask', 'SQLALCHEMY_TRACK_MODIFICATIONS')
    LogTool.info(f"{ConfigTool.get_dict('flask', 'SQL_CONN')}")
    db_dict, default = FlaskConnTool.get_oracle_dict(ConfigTool.get_dict('flask', 'SQL_CONN'))
    LogTool.info(f"数据库连接；【{db_dict}】【{default}】")
    app.config['SQLALCHEMY_DATABASE_URI'] = default
    app.config['SQLALCHEMY_BINDS'] = db_dict
    app.config['USE_RELOADER'] = ConfigTool.get_bool('flask', 'USE_RELOADER')
    app.config['SECRET_KEY'] = 'secret!'


def __init_db():
    """
    初始化数据库连接
    :return:
    """
    from lbj_flask.extensions import db
    db.init_app(app)
    db.app = app

    from lbj_db.db_base_tool import DBBaseTool
    DBBaseTool.init_db(db)
    DBBaseTool.init_page(1, 15, 'PAGE_ROW_CNT', 'DEFAULT', 'tbl')


def __init_home():
    """
    初始化hi
    :return:
    """
    import project.app.home


def __init_print():
    """
    打印输出
    :return:
    """
    from lbj_common.config_tool import ConfigTool
    from lbj_common.log_tool import LogTool
    LogTool.print("------------------启动项目-----------------------------")
    LogTool.print(f"平台信息：   【{platform.platform()}】")
    LogTool.print(f"当前路径：   【{os.getcwd()}】")
    LogTool.print(f"系统变量：   【{sys.path}】")
    LogTool.print(f"日志路径：   【{LogTool.path}】")
    LogTool.print(f"main路径：   【{ConfigTool.get_path()}】")
    LogTool.print(f"python路径： 【{sys.executable}】")
    LogTool.print(f"__file__路径： 【{__file__}】")
    LogTool.print(f"sys.argv路径： 【{sys.argv}】")
    LogTool.print("初始化完成")


def __init_socket():
    """
    初始化socket
    :return:
    """
    import project.app.socket.api


def __init():
    __init_env()
    __init_log()
    __init_app_config()
    __init_db()
    __init_home()
    __init_print()




__init()
# 含有socket方式
# from flask_socketio import SocketIO
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', engineio_logger=True, debug=True)
# __init_socket()


@app.route('/')
def index():
    """
    首页测试
    :return:
    """
    return 'security_center'


@app.route('/health')
def health():
    """
    心跳 对接springcloud
    :return:
    """
    t = {'status': 'UP'}
    return Response(json.dumps(t), mimetype='application/json')


@app.before_request
def before_request():
    """
    全局请求过滤
    :return:
    """
    from lbj_flask.request_tool import RequestTool
    return RequestTool.handle_request()


@app.after_request
def after_request(response):
    """
    全局返回过滤
    :param response:
    :return:
    """
    from lbj_flask.response_tool import ResponseTool
    return ResponseTool.handle_response(response)


# 注册蓝本
# 认证中心
from project.app.api import blueprint_authority

app.register_blueprint(blueprint_authority)
