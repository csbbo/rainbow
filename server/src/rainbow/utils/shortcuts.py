import json
import os
import random
from collections import OrderedDict
import datetime

from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string


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


def delete_file(filename, path=settings.PHOTOS_PATH):
    file_path = os.path.join(path, filename)
    if os.path.exists(file_path):
        os.remove(file_path)


def save_file(filename, file, path=settings.PHOTOS_PATH):
    with open(os.path.join(path, filename), 'wb+') as fp:
        for chunks in file.chunks():
            fp.write(chunks)


def rand_str(length=32, type="lower_hex"):
    if type == "str":
        return get_random_string(length, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    elif type == "lower_str":
        return get_random_string(length, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789")
    elif type == "lower_hex":
        return random.choice("123456789abcdef") + get_random_string(length - 1, allowed_chars="0123456789abcdef")
    elif type == "letter":
        return get_random_string(length, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    else:
        return random.choice("123456789") + get_random_string(length - 1, allowed_chars="0123456789")
