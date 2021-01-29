
from setuptools import setup, find_packages

setup(
    name='lbj-flask',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        "gevent==1.4.0",
        "gunicorn==19.9.0",
        "requests==2.18.4",
        "flask==0.12.1",
        "flask-restful==0.3.6",
        "flask-sqlalchemy==2.3.0",
        "flask-cors==3.0.4",
        "Werkzeug==0.15"
    ],
    description='Flask公共插件',
    url='None',
    author='李宝杰',
    author_email='libaojie@qq.com',
)