from lhzl_common.decorator import log_fun
from lhzl_common.log_tool import LogTool
from sqlalchemy import create_engine

from lhzl_db.db_engine_tool import DBEngineTool
from lhzl_db.df.df_db_tool import DFDBTool


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
    LogTool.init("./data")
    test_insert()

@log_fun
def test_insert():
    """
    测试插入
    :return:
    """
    db = create_engine("oracle://lhzlibm:D_Matibm#2018@192.168.160.231:1521/orcl")
    DBEngineTool.init_db(db)

    import numpy as np
    import pandas as pd

    # 生成樣例數據
    def gen_sample(row):
        aaa = np.random.uniform(1, 1000, row)
        return pd.DataFrame({'id': aaa})

    df = gen_sample(1000000)

    DFDBTool.df_to_db("testIBM_COEF", df)

    ret = DBEngineTool.find_count("select count(id) from testIBM_COEF")
    print(ret)

    assert ret > 0


test()
