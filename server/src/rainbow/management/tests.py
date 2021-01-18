import random

from photo.models import Photo
from utils.constans import PhotoTypeEnum
from utils.shortcuts import rand_str
from utils.tests import APITestCase


class GuestBookAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("GuestBookAPI")
        # self.create_user(username='bob', password='123456', login=True)

    def test_leave_message(self):
        resp = self.post(self.url, {'content': 'leave a message...'})
        self.assertSuccess(resp)


class MainPageAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url('MainPageAPI')
        data = {
            'name': f'rainbow',
            'description': f'the photo 0 description',
            'copyright': 'rainbow',
            'category': [PhotoTypeEnum.bing, ],

            'save_name': rand_str(32),
            'upload_name': f'rainbow',

            'watch_count': random.randint(0, 100),
            'thumb_count': random.randint(0, 100),
            'download_count': random.randint(0, 100),
        }
        Photo.objects.create(**data)

    def test_get_mainpage_api(self):
        resp = self.get(self.url)
        self.assertSuccess(resp)
        self.pprint(resp)
