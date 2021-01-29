
from setuptools import setup, find_packages

setup(
    name='lbj-excel',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        "xlrd==1.1.0",
        "xlutils==2.0.0",
        "xlwt==1.3.0"
    ],
    description='基础工具包',
    url='None',
    author='李宝杰',
    author_email='libaojie@qq.com',
)


