
from setuptools import setup, find_packages

setup(
    name='lbj-db',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        "sqlalchemy ==1.2.0",
        "pymysql==0.8.0",
        "cx-oracle==6.2.1"
    ],
    description='数据库连接中间层',
    url='None',
    author='李宝杰',
    author_email='libaojie@qq.com',
)