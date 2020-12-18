from photo.models import Photo
from utils.constans import PhotoTypeEnum
from utils.tests import APITestCase


class PhotoAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("PhotoListAPI")

        for i in range(10):
            Photo.objects.create(**{'name': f'bing{i}', 'category': [PhotoTypeEnum.bing]})
            Photo.objects.create(**{'name': f'infinity_anime{i}', 'category': [PhotoTypeEnum.infinity, PhotoTypeEnum.anime]})
            Photo.objects.create(**{'name': f'infinity_landscape{i}', 'category': [PhotoTypeEnum.infinity, PhotoTypeEnum.landscape]})

    def test_get_photos(self):
        data = {
            'category': [PhotoTypeEnum.bing, PhotoTypeEnum.anime],
            'offset': 0,
            'count': 10
        }
        resp = self.client.get(self.url, data=data)
        self.assertSuccess(resp)
