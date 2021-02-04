# Flask下mysqldb不支持python3，需要pymysql转一下
import platform

import pymysql

pymysql.install_as_MySQLdb()

import sqlalchemy.sql.default_comparator
import sqlalchemy.ext.baked

if 'Linux' in platform.platform():
    import gevent
    from gevent import monkey

    gevent.monkey.patch_all()
