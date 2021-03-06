import os
import sys

from lbj_common.config_tool import ConfigTool
from lbj_common.log_tool1 import LogTool
from lbj_common.time_tool import TimeTool

try:
    mainroot = os.path.dirname(os.path.abspath(__file__))
except NameError:
    mainroot = os.path.dirname(os.path.abspath(sys.argv[0]))

ConfigTool.set_path(mainroot)
LogTool.init(mainroot)

LogTool.info(f"{TimeTool.get_currer_time()}")