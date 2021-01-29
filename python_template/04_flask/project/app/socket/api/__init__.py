#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : socket消息
@Time       : 2019/10/22 14:39
@Author     : zsl
@File       : __init__.py
@Software   : PyCharm
"""
import json

import requests
from flask import request, session, Blueprint
from flask_restful import Api
#from flask_socketio import join_room, disconnect, emit

#from project.app import socketio
from lbj_common.log_tool import LogTool

blueprint_ws = Blueprint("api_ws", __name__, url_prefix='/ws/v1/socket')


@blueprint_ws.before_request
def before_request():
    """
    当前蓝图拦截
    :return:
    """

    return None


# @socketio.on('send_server', namespace='/ws/v1/socket')
def send_server(mess):
    # message = [mess['data']]
    LogTool.info('测试 client发送消息!!!')
    # emit('send_client',
    #      {'data': {'message': ['成功接收，请放心！'], 'count': 0}, 'type': '1'})


# @socketio.on('disconnect', namespace='/ws/v1/socket')
def try_disconnect():
    session['receive_count'] = session.get('receive_count', 0) + 1
    # emit('send_client',
    #      {'data': {'message': ['断开连接，请注意！'], 'count': 0}, 'type': '0'})
    # disconnect()


# @socketio.on('send_room', namespace='/ws/v1/socket')
def send_room(room, infos, send_type='0', namespace='/ws/v1/socket'):
    # 如果有消息，格式转换，全部推送给当前room 的所有人
    count = session.get('receive_count', 0) + 1

    # emit('send_client', _ret_data, room=room, namespace=namespace)


# @socketcketio.on('connect', namespace='/ws/v1/socket')
def try_connect():
    # 获取token信息
    pass


