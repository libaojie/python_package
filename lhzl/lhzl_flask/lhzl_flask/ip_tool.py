#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 
@Time       : 2019/8/15 16:31
@Author     : libaojie
@File       : ip_tool.py
@Software   : PyCharm
"""
import socket

from lhzl_common.log_tool import LogTool


class IpTool(object):

    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip

    @staticmethod
    def get_ip(request):

        # 遍历request.headers，打印所有参数
        ip = request.headers.get('x-forwarded-for')
        if ip is None or len(ip) == 0 or 'unknown' == ip.lower():
            ip = request.headers.get("Proxy-Client-IP")
        if ip is None or len(ip) == 0 or 'unknown' == ip.lower():
            ip = request.headers.get("WL-Proxy-Client-IP")
        if ip is None or len(ip) == 0 or 'unknown' == ip.lower():
            ip = request.headers.get("HTTP_CLIENT_IP")
        if ip is None or len(ip) == 0 or 'unknown' == ip.lower():
            ip = request.headers.get("HTTP_X_FORWARDED_FOR")
        if ip is None or len(ip) == 0 or 'unknown' == ip.lower():
            ip = request.headers.get("X-Real-IP")
        if ip is None or len(ip) == 0 or 'unknown' == ip.lower():
            ip = request.host.split(':')[0]
        if '0:0:0:0:0:0:0:1' == ip:
            ip = "127.0.0.1"
        # 有些网络通过多层代理，那么获取到的ip就会有多个，一般都是通过逗号（, ）分割开来，并且第一个ip为客户端的真实IP
        if ip is not None and len(ip) > 0:
            ip = ip.split(',')[0]
        LogTool.info(f"获取ip【{ip}】")
        return ip
