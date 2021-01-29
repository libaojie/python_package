from lbj_flask.entity.entity_base import EntityBase
from lbj_flask.enum.del_flag import DelFlag
from lbj_flask.extensions import db
from lbj_flask.orm_tool import OrmTool


class RestfulModel(EntityBase, db.Model):

    __bind_key__ = 'db_key'
    __tablename__ = 'tbl_name'
    name = db.Column(db.String)  # 监测点名称

    @classmethod
    def find_by_orm(cls, page, per_page, id, name):
        return OrmTool.find_by_query(cls, page, per_page,
                                     precise_dict={'del_flag': DelFlag.view.value, 'id': id},
                                     fuzzy_dict={'name': name})
