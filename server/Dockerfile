FROM ubuntu:20.04

COPY requirements.txt /tmp/requirements.txt

ADD ./src/rainbow /web

RUN printf "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse\ndeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse\ndeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse\ndeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse\n" > /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y python3.8 python3.8-dev python3-pip libpq-dev vim \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /tmp/requirements.txt \
    && ln -sfv /web/rainbow/settings.py.pro /web/rainbow/settings.py \
    && ln -sfv /usr/local/bin/dramatiq /usr/bin/dramatiq

WORKDIR /web

CMD bash /web/run.sh
