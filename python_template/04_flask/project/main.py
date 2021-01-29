#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

from lbj_common.config_tool import ConfigTool

try:
    mainroot = os.path.dirname(os.path.abspath(__file__))
except NameError:
    mainroot = os.path.dirname(os.path.abspath(sys.argv[0]))

ConfigTool.set_path(mainroot)

if __name__ == '__main__':
    from project.app import app

    app.run(host=ConfigTool.get_str("app", "HOST"), port=ConfigTool.get_int("app", "PORT"), threaded=True)

    # socketio启动方式
    # from project.app import socketio
    # socketio.run(app, host=ConfigTool.get_str("app", "HOST"), port=ConfigTool.get_int("app", "PORT"))
