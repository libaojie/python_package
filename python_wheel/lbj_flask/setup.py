from setuptools import setup, find_packages

setup(
    name='lbj-flask',
    version='2.0',
    packages=find_packages(),
    setup_requires=['flask', 'flask-restful', 'flask-sqlalchemy', 'Werkzeug'],
    install_requires=[
        "gevent>=22.10.1",
        "gunicorn>=20.1.0",
        "requests>=2.28.1",
        "flask>=2.0.3",
        "flask-restful>=0.3.9",
        "flask-sqlalchemy>=2.5.1",
        "flask-cors>=3.0.4",
        "Werkzeug>=2.2.2",
    ],
    description='Flask公共插件',
    url='None',
    author='李宝杰',
    author_email='libaojie@qq.com',
)
