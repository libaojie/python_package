from enum import Enum


class DelFlag(Enum):
    """
    是否删除枚举
    """
    # 全部
    all = None
    view = '0'
    delete = '1'