from enum import Enum, unique


class ErrorCodeImpl(Enum):
    """
    错误码的公共方法
    """

    def get_code(self):
        """
        获取状态码code
        :return: code
        """
        tup = self.value.items()
        return list(self.value.keys())[0]

    def get_msg(self):
        """
        获取状态信息message
        :return: message
        """
        return list(self.value.values())[0]


@unique
class ErrorCode(ErrorCodeImpl):
    """
    统一错误码
    """

    SUCCESS = {"0": "成功"}
    FAILURE = {"1": "失败"}

    REQ_IS_NONE = {"21": "request不能为空"}
    HEADER_TYPE_SETTING = {"22": "请求头请设置为application/json"}
    JSON_ERROR = {"23": "传入的json格式有误"}
    DB_ERROR = {"30": "数据库操作失败"}

    UNKNOWN_ERROR = {"100101": "未知错误"}
    HAVE_NOT_REQ = {"100102": "没有获取到请求"}
    PARAM_LACK = {"100103": "缺少必要参数"}
    PARAM_NONE = {"100104": "必要参数不能为空"}
    PARAM_ILLEGAL = {"100105": "非法参数"}
    PARAM_MISS = {"100106": "请求参数为空"}

    # 数据库相关
    NOT_FOUND = {"100201": "未查询到数据"}
    INSERT_FAILURE = {"100202": "新增数据失败"}
    UPDATE_FAILURE = {"100203": "修改数据失败"}
    DELETE_FAILURE = {"100204": "删除数据失败"}
    UNIQUE_SETTING = {"100205": "违反唯一性约束"}

    # 文件相关
    FILE_UPLOAD_FAILURE = {"100301": "文件上传失败"}
    FILE_DOWNLOAD_FAILURE = {"100302": "文件下载失败"}
    FILE_SAVE_FAILURE = {"100303": "文件保存失败"}
    FILE_NONE = {"100304": "未找到此文件"}
    FILE_IS_NONE = {"100305": "不是文件"}
    FILE_PATH_NOT_EXISTS = {"100306": "文件目录不存在"}
