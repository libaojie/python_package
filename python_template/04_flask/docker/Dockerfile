FROM centos:7.2.1511
# author label
LABEL maintainer="libaojie"


# install related packages
ENV ENVIRONMENT DOCKER_PROD
RUN cd / && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && yum makecache \
    && yum install -y wget aclocal automake autoconf make gcc gcc-c++ python-devel mysql-devel bzip2 libffi-devel epel-release \
    && yum clean all

RUN rpm --rebuilddb && yum install -y  mesa-libGL  \
    && yum clean all

# install python 3.7.4
COPY Python-3.7.4.tar.xz .
RUN tar -xvf Python-3.7.4.tar.xz -C /usr/local/ \
    && rm -rf Python-3.7.4.tar.xz \
    && cd /usr/local/Python-3.7.4 \
    && ./configure --prefix=/usr/local/python3 --with-ssl && make && make install \
    #&& mv /usr/bin/python /usr/bin/python_old \
    && ln -s /usr/local/python3/bin/python3 /usr/bin/python3 \
    && python3 -m pip install --upgrade pip \
    && rm -rf /usr/local/Python-3.7.4

#RUN python3 -m pip install setuptools==19.2.0 -i http://192.168.160.232:11004/repository/pypi-group/simple/ --trusted-host 192.168.160.232

# 安装依赖
ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt -i http://192.168.160.232:11004/repository/pypi-group/simple/ --trusted-host 192.168.160.232

# 处理ModuleNotFoundError: No module named '_lzma'
RUN yum install -y xz-devel python-backports-lzma \
    && python3 -m pip install backports.lzma \
    && yum clean all
ADD lzma.py.bak /usr/local/python3/lib/python3.7/lzma.py


# expost port
EXPOSE 15020