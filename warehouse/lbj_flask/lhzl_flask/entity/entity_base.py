#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Comment    : 模型基类
@Time       : 2018/6/12 17:05
@Author     : libaojie
@File       : model.py
@Software   : PyCharm
"""
from lhzl_common.config_tool import ConfigTool
from lhzl_common.log_tool import LogTool
from lhzl_common.time_tool import TimeTool
from lhzl_common.utils import Utils
from lhzl_db.db_session_tool import DBSessionTool

from lhzl_flask.enum.del_flag import DelFlag
from lhzl_flask.extensions import db
from lhzl_flask.orm_tool import OrmTool
from lhzl_flask.user_tool import UserTool


class EntityBase(object):
    """
    实体表基类
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(256), primary_key=True)
    del_flag = db.Column(db.String(1))
    create_time = db.Column(db.DateTime())
    create_user = db.Column(db.String(256))
    update_time = db.Column(db.DateTime())
    update_user = db.Column(db.String(256))
    remark = db.Column(db.String(500))

    def __init__(self, create_user=None, update_user=None, remark=''):
        self.id = Utils.get_uuid()
        self.del_flag = DelFlag.view.value
        cur_time = TimeTool.get_currer_time()
        self.create_time = cur_time
        self.update_time = cur_time
        self.remark = remark
        if create_user:
            self.create_user = create_user
        elif UserTool.get_login_user():
            self.create_user = UserTool.get_user_id()
        else:
            self.create_user = None

        if update_user:
            self.update_user = update_user
        elif UserTool.get_login_user():
            self.update_user = UserTool.get_user_id()
        else:
            self.update_user = None

    def __repr__(self):
        return f"类：【{self.__class__.__name__}】 值：【{self.__dict__}】"

    @classmethod
    def find(cls, del_flag=DelFlag.view.value):
        """
        查找所有记录
        :param id:
        :return:
        """
        _ret = cls.query
        # 数据状态
        if del_flag != DelFlag.all.value:
            return _ret.filter(cls.del_flag == del_flag).all()
        return _ret.filter().all()

    @classmethod
    def paginate(cls, page_num, page_size):
        return OrmTool.find_by_query(cls, page_num, page_size,
                                     precise_dict={'del_flag': DelFlag.view.value, 'id': id})

    @classmethod
    def get_by_id(cls, id, del_flag=DelFlag.view.value):
        """
        通过id找到某条记录
        :param id:
        :return:
        """
        _ret = cls.query
        # 数据状态
        if del_flag != DelFlag.all.value:
            _ret = _ret.filter(cls.del_flag == del_flag)
        return _ret.filter(cls.id == id).first()

    @classmethod
    def is_exist(cls, id, del_flag=DelFlag.view.value):
        """
        数据是否存在
        :param id:
        :return:
        """
        return False if cls.get_by_id(id, del_flag) is None else True

    def save(self):
        """
        保存某条记录
        :param commit:
        :return:
        """
        LogTool.info(f"数据库【{self.__tablename__}】表写入数据！")
        db.session.add(self)
        if not DBSessionTool.flush():
            LogTool.error(f"【{self.__tablename__}】表保存失败")
            return False
        return True

    def delete(self):
        """
        删除某条记录
        :param commit:
        :return:
        """
        LogTool.info(f"数据库【{self.__tablename__}】表删除数据！")
        self.del_flag = DelFlag.delete.value
        return self.update()

    def update(self):
        """
        更新某条记录
        :return:
        """
        LogTool.info(f"数据库【{self.__tablename__}】更新数据！")
        self.update_time = TimeTool.get_currer_time()
        if UserTool.get_login_user():
            self.update_user = UserTool.get_user_id()

        if not DBSessionTool.flush():
            LogTool.error(f"【{self.__tablename__}】表更新失败")
            return False
        return True

    def as_dict(self):
        """
        核心数据组织json
        :return:
        """
        return {'id': self.id, 'updateTime': self.update_time}
