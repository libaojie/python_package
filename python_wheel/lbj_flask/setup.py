
from setuptools import setup, find_packages

setup(
    name='lbj-flask',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        "gevent==1.4.0",
        "gunicorn==19.9.0",
        "requests==2.18.4",
        "flask==2.0.3",
        "flask-restful==0.3.9",
        "flask-sqlalchemy==2.3.0",
        "flask-cors==3.0.4",
        "Werkzeug==2.0"
    ],
    description='Flask公共插件',
    url='None',
    author='李宝杰',
    author_email='libaojie@qq.com',
)