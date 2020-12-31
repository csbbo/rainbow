import datetime
import logging
import os

import pytz
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup

from photo.management.commands.fetch_bing import save_remote_image
from photo.models import Photo
from utils.constans import Choices, PhotoTypeEnum
from utils.shortcuts import rand_str

logger = logging.getLogger(__name__)

host = 'https://bing.ioliu.cn'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}


def get_detail_page_url():
    detail_pages_url = []
    page = 1
    while True:
        url = f'{host}/?p={page}'
        r = requests.get(url, headers=headers)
        bf = BeautifulSoup(r.text, 'lxml')
        marks = bf.find_all('a', 'mark')
        for mark in marks:
            detail_pages_url.append(host + mark.get('href'))

        if len(marks) < 12 or page > 200:
            break
        page += 1
    return list(set(detail_pages_url))


def get_photo_data():
    page_urls = get_detail_page_url()
    data_list = []
    for page_url in page_urls:
        r = requests.get(page_url, headers=headers)
        bf = BeautifulSoup(r.text, 'lxml')
        photo_name = bf.find('a', {'class': 'download'})['href'].split('/')[-1].split('?')[0]
        data_list.append({
            'photo_title': bf.find('p', {'class': 'title'}).get_text(),
            'photo_time': bf.find('p', {'class': 'calendari'}).find('em', {'class': 't'}).get_text(),
            'photo_path': f'http://h2.ioliu.cn/bing/{photo_name}_1920x1080.jpg',
        })
    return data_list


def sync_remote_image():
    images = get_photo_data()
    for img in images:
        create_time = datetime.datetime.strptime(img['photo_time'], '%Y-%m-%d')
        create_time = pytz.timezone(settings.TIME_ZONE).localize(create_time)
        if not Photo.objects.filter(create_time=create_time, category__contains=[PhotoTypeEnum.bing, ]).exists():
            name = img['photo_title'].split('(')[0].split('，')[0]
            save_name = rand_str(32)
            photo = Photo.objects.create(name=name,
                                         save_name=save_name,
                                         copyright=img['photo_title'],
                                         category=[PhotoTypeEnum.bing],
                                         create_time=create_time)
            try:
                save_remote_image('https://bing.com' + img['photo_path'], name=save_name)
            except Exception as e:
                photo.delete()
                logger.error("save image fail with error: " + str(e))


class Command(BaseCommand):
    help = "Synchronous Bing wallpaper"

    def add_arguments(self, parser):
        parser.add_argument("sub_command", nargs="?", type=str, help="The sub command")

    def handle(self, *args, **options):
        sync_remote_image()
