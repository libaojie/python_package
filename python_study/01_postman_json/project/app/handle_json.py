import re

from lbj_common.file_tool import FileTool
from lbj_common.log_tool import LogTool


class HandleJson(object):

    def handle(self, path):
        """
        将postman的json文件解析出  服务地址
        :return:
        """
        content = FileTool.open_file(path)

        items = re.findall("\"item\":\W+\[(.+)\]", content, re.S)

        for item in items:
            its = re.findall("{\W+?(\"name\".+?)\"response\":\W+?\[", item, re.S)
            LogTool.print(f"名称\t方式\t路径\t")
            for it in its:
                name = re.findall(
                    "\"name\"\W+?\"(.+?)\",.+?\"method\":\W+?\"(.+?)\",.+?\"raw\":\W+?\"http://.+?/(.+?)\"", it, re.S)
                LogTool.print(f"{name[0][0]}\t{name[0][1]}\t/{name[0][2]}\t")
