from sqlalchemy import create_engine

from lhzl_db.db_engine_tool import DBEngineTool


def test():
    # db = 1
    # page_num = 5
    # page_size = 6
    # page_code = 'code'
    # page_key  = 'key'
    # dict_tbl_name = 'lhzlmr.mr_dict'
    # db = create_engine("oracle://lhzlca:D_Matca#2018@192.168.160.231:1521/orcl")
    # DBEngineTool.init_db(db)
    # ret = DBEngineTool.find_by_sql("select * from ca_application", 4, 5)
    # print(ret)
    test_conn()


def test_conn():
    """
    测试连接
    :return:
    """
    db = create_engine("oracle://lhzlca:D_Matca#2018@192.168.160.231:1521/orcl")
    DBEngineTool.init_db(db)
    ret = DBEngineTool.find_by_sql("select * from ca_application", 4, 5)
    assert len(ret.data) == 0


test()