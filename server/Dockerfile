FROM ubuntu:20.04

COPY requirements.txt /tmp/requirements.txt

ADD ./src/rainbow /web

RUN apt-get update \
    && apt-get install -y python3.8 python3.8-dev python3-pip libpq-dev vim \
#    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /tmp/requirements.txt \
    && pip3 install -r /tmp/requirements.txt \
    && ln -sfv /web/rainbow/settings.py.pro /web/rainbow/settings.py

WORKDIR /web

CMD bash /web/run.sh
