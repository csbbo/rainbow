import logging
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from photo.models import Photo
from utils.constans import Choices, PhotoTypeEnum
from utils.shortcuts import save_remote_image, delete_file

logger = logging.getLogger(__name__)


class SubCommandTypeEnum(Choices):
    fetch_now = "fetch_now"
    crontab = "crontab"


def get_image_info(url):
    proxies = {
        'https': None
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    r = requests.get(url, proxies=proxies, headers=headers)
    resp = r.json()
    images = resp['data']

    data_list = []
    for img in images:
        data_list.append({'url': img['src']['rawSrc']})
    return data_list


def sync_anime_image():
    url = 'https://infinity-api.infinitynewtab.com/get-wallpaper?source=Infinity'
    images = get_image_info(url)
    photos = Photo.objects.filter(category__contains=[PhotoTypeEnum.anime, ])
    for photo in photos:
        delete_file(str(photo.id), path=settings.PHOTOS_PATH)
        photo.delete()

    for img in images:
        photo = Photo.objects.create(category=[PhotoTypeEnum.anime, ])
        try:
            save_remote_image(img['url'], str(photo.id))
        except Exception as e:
            photo.delete()
            logger.error("save image fail with error: " + str(e))


def sync_landscape_image():
    url = 'https://infinity-api.infinitynewtab.com/get-wallpaper?source=InfinityLandscape'
    images = get_image_info(url)
    photos = Photo.objects.filter(category__contains=[PhotoTypeEnum.landscape, ])
    for photo in photos:
        delete_file(str(photo.id), path=settings.PHOTOS_PATH)
        photo.delete()

    for img in images:
        photo = Photo.objects.create(category=[PhotoTypeEnum.landscape, ])
        try:
            save_remote_image(img['url'], str(photo.id))
        except Exception as e:
            photo.delete()
            logger.error("save image fail with error: " + str(e))


class Command(BaseCommand):
    help = "Synchronous Infinity wallpaper"

    def handle(self, *args, **options):
        sync_anime_image()
        sync_landscape_image()
