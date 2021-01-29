from lbj_common.log_tool import LogTool

from lbj_db.conn.db_conn_tool import DBConnTool


class FlaskConnTool(object):
    """
    Flask连接数据库的方式
    """

    @classmethod
    def get_mysql_dict(cls, conn_str):
        """
        获取mysql的数据字典
        :param conn_str:  形如 {'oracle_lbjmr': {'ip': '192.168.160.231', 'port': '1521', 'uname': 'lbjmr', 'pwd': '****', 'sname': 'orcl'}
        :return:
        """
        if conn_str is None:
            LogTool.error("数据路连接字符串不能为空")
            return None
        default = None
        ret = {}
        for key, value in conn_str.items():
            db = DBConnTool.get_mysql_conn_str(value.get('ip'),
                                               value.get('port'),
                                               value.get('uname'),
                                               value.get('pwd'),
                                               value.get('dbname'))
            if db is not None:
                ret[key] = db
                if default is None:
                    default = db
        return ret, default

    @classmethod
    def get_oracle_dict(cls, conn_str):
        """
        获取oracle的数据字典
        :param conn_str:    形如 {'oracle_lbjmr': {'ip': '192.168.160.231', 'port': '1521', 'uname': 'lbjmr', 'pwd': '****', 'sname': 'orcl'}
        :return:
        """
        if conn_str is None:
            LogTool.error("数据路连接字符串不能为空")
            return None
        default = None
        ret = {}
        for key, value in conn_str.items():
            db = DBConnTool.get_oracle_conn_str(value.get('ip'),
                                                value.get('port'),
                                                value.get('uname'),
                                                value.get('pwd'),
                                                value.get('sid'),
                                                value.get('sname'))
            if db is not None:
                ret[key] = db
                if default is None:
                    default = db
        return ret, default
