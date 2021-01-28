import logging
import requests
import urllib
import json
import time
from functools import wraps
from multiprocessing import Pool

logger = logging.getLogger(__name__)
requests.packages.urllib3.disable_warnings()


def cost_time(func):
    @wraps(func)
    def wrapper(*args, **kw):
        now = time.time()
        func(*args, **kw)
        print(f'{func.__name__} cost time: {time.time() - now} second')
    return wrapper


@cost_time
def photo_list():
    url = 'https://rainbow.shaobo.fun' + '/api/PhotoListAPI?count=12&offset=0'
    r = requests.get(url)
    print(r.json())


if __name__ == '__main__':
    photo_list()
