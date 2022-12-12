FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV TimeZone=Asia/Shanghai 

# 添加 Debian 清华镜像源
RUN echo \
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free\
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free\
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free\
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free\
    > /etc/apt/sources.list

# 添加这两行
RUN apt-get update
RUN apt-get install libpython3-dev default-libmysqlclient-dev build-essential -y

RUN mkdir /django
WORKDIR /django
RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY /myProject /django
COPY requirements.txt /django
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

