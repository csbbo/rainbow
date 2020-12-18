import json
import os
from collections import OrderedDict
from datetime import datetime

import requests
from django.conf import settings
from django.utils import timezone


def datetime_pretty(value=None, *, fmt="%Y-%m-%d %H:%M:%S %Z"):
    """
    :param value: 时间，如果是 None 就返回当前时间
    :param fmt: 返回时间的格式
    """
    return timezone.localtime(value, timezone=None).strftime(fmt)


class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        if isinstance(o, OrderedDict):
            return dict(o)
        if isinstance(o, datetime.datetime):
            return datetime_pretty(o)
        return json.JSONEncoder.default(self, o)


def save_remote_image(url, img_name, path=settings.PHOTOS_PATH):
    """
    :param url: 图片网络地址
    :param img_name: 图片名
    :param path: 保存路径
    """
    if not os.path.exists(path):
        os.makedirs(path)
    save_path = os.path.join(path, img_name)

    with requests.get(url, timeout=30, stream=True) as r:
        with open(save_path, 'wb') as f:
            for d in r.iter_content(128):
                f.write(d)


def delete_file(filename, path):
    file_path = os.path.join(path, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
