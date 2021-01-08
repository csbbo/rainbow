import datetime
import logging
import os

import pytz
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.core.management.base import BaseCommand

from photo.models import Photo
from photo.utils import get_image_dpi
from utils.constans import Choices, PhotoTypeEnum
from utils.shortcuts import rand_str

logger = logging.getLogger(__name__)


class SubCommandTypeEnum(Choices):
    fetch_now = "fetch_now"
    crontab = "crontab"


def save_remote_image(url, name, path=settings.PHOTOS_PATH):
    """
    :param url: 图片网络地址
    :param img_name: 图片名
    :param path: 保存路径
    """
    if not os.path.exists(path):
        os.makedirs(path)
    save_path = os.path.join(path, name)

    with requests.get(url, timeout=30, stream=True) as r:
        with open(save_path, 'wb') as f:
            for d in r.iter_content(128):
                f.write(d)


def get_image_info(date: int = 0, nums: int = 8):
    url = f'https://www.bing.com/HPImageArchive.aspx?format=js&idx={date}&n={nums}&nc=1607762051663&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160'
    proxies = {
        'https': None
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    r = requests.get(url, proxies=proxies, headers=headers)
    resp = r.json()
    images = resp['images']

    data_list = []
    for img in images:
        data_list.append({
            'enddate': img['enddate'],
            'url': img['url'],
            'copyright': img['copyright'],
        })
    return data_list


def sync_remote_image():
    images = get_image_info()
    for img in images:
        create_time = datetime.datetime.strptime(img['enddate'], '%Y%m%d')
        create_time = pytz.timezone(settings.TIME_ZONE).localize(create_time)
        if not Photo.objects.filter(create_time=create_time, category__contains=[PhotoTypeEnum.bing, ]).exists():
            name = img['copyright']
            save_name = rand_str(32)
            try:
                save_remote_image('https://bing.com' + img['url'], name=save_name)
                dpi = get_image_dpi(save_name)
                new_photo = {
                    'name': name,
                    # 'description': None,
                    # 'location': 'Beijing',
                    # 'copyright': copyright,
                    'category': [PhotoTypeEnum.bing],
                    'dpi': dpi,
                    'save_name': save_name,
                    'create_time': create_time
                }
                Photo.objects.create(**new_photo)
            except Exception as e:
                logger.error("save image fail with error: \n" + str(e))


class Command(BaseCommand):
    help = "Synchronous Bing wallpaper"

    def add_arguments(self, parser):
        parser.add_argument("sub_command", nargs="?", type=str, help="The sub command")

    def handle(self, *args, **options):
        sub_command = options['sub_command']

        if sub_command not in SubCommandTypeEnum.choices():
            self.stdout.write("command not found")
            return

        if sub_command == SubCommandTypeEnum.fetch_now:
            sync_remote_image()
            return

        if sub_command == SubCommandTypeEnum.crontab:
            scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

            scheduler.add_job(sync_remote_image, 'cron', day_of_week='0-6', hour=0, minute=0, second=30)
            logger.info("Added job 'update_stocks'.")

            try:
                logger.info("Starting scheduler...")
                scheduler.start()
            except KeyboardInterrupt:
                logger.info("Stopping scheduler...")
                scheduler.shutdown()
                logger.info("Scheduler shut down successfully!")
            return
