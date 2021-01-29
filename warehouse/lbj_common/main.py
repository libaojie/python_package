import os
import shutil

"""
打包
"""


def _delete_file_path(input_path):
    """
    删除原文件夹
    :param input_path:
    :return:
    """
    if os.path.isdir(input_path):
        shutil.rmtree(input_path)

_delete_file_path("./build")
# os.system("python -m pipenv run python setup.py bdist_wheel")
os.system("python -m poetry run python setup.py bdist_wheel")