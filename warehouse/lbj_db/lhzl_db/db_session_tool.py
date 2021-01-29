from lhzl_common.decorator import log_fun
from lhzl_common.log_tool import LogTool

from lhzl_db.db_base_tool import DBBaseTool
from lhzl_db.entity.ret_run_sql import RetRunSql


class DBSessionTool(DBBaseTool):
    """
    数据库操作基类
    """

    def __init__(self):
        super().__init__()
        pass

    @classmethod
    def _get_session(cls):
        if cls.db_session is None:
            LogTool.error(f"Session初始化失败！")
        return cls.db_session

    @classmethod
    def commit(cls):
        """
        session提交
        :return:
        """
        if cls._get_session() is None:
            return None

        try:
            cls._get_session().commit()
            LogTool.info("提交session成功")
            return True
        except Exception as e:
            cls._get_session().rollback()
            LogTool.error(f"Session提交问题；【{str(e)}】")
            return False
        finally:
            pass

    @classmethod
    def flush(cls):
        """
        session刷新
        :return:
        """
        if cls._get_session() is None:
            return None

        try:
            cls._get_session().flush()
            LogTool.info("数据库更新成功！")
            return True
        except Exception as e:
            cls._get_session().rollback()
            LogTool.error(f"Session刷新问题；【{str(e)}】")
            return False

    @classmethod
    @log_fun
    def run_sql(cls, sql):
        """
        运行sql
        :param sql:
        :return:
        """
        if cls._get_session() is None:
            return None

        sql = sql.replace('\n', '')
        retRunSql = RetRunSql()
        try:
            # LogTool.info('执行sql：{0}'.format(sql))
            ret = cls._get_session().execute(sql)  # 执行数据插入操作
            try:
                retRunSql.col_list = ret._metadata.keys
                # retRunSql.col_list = [r for r in ret._metadata.keys]
                count = ret.rowcount
                retRunSql.val_list = ret.fetchall()
                retRunSql.is_success = True
            except Exception as e:
                LogTool.error(f"执行sql解析结果【{str(e)}】；【{sql}】")
                pass
            finally:
                cls.flush()
                # LogTool.info(f"执行sql结束")
                return retRunSql
        except Exception as e:
            cls._get_session().rollback()  # 异常则回滚
            LogTool.error(f"执行数据库报错：【{e}】")
            LogTool.error(f"sql：【{sql}】")
            return retRunSql
        finally:
            # cursor.close()
            # LogTool.info(f"执行sql结束")
            pass
