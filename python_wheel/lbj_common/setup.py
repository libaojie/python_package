
from setuptools import setup, find_packages

setup(
    name='lhzl-common',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        "setuptools==19.2.0",
        "wheel==0.34.2",
        "pandas==0.23.4",
        "docxtpl==0.4.13",
        "xlrd==1.1.0",
        "xlutils==2.0.0",
        "xlwt==1.3.0"
    ],
    description='基础工具包',
    url='None',
    author='李宝杰',
    author_email='libaojie@qq.com',
)


