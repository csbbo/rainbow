import base64
import random
import tempfile

from photo.models import Photo
from utils.constans import PhotoTypeEnum
from utils.shortcuts import rand_str
from utils.tests import APITestCase


def create_test_data(data_count=10):
    data_list = []
    for i in range(data_count):
        data = {
            'name': f'rainbow{i}',
            'description': f'the photo {i} description',
            'copyright': 'rainbow',
            'category': PhotoTypeEnum.choices()[:random.randint(1, len(PhotoTypeEnum.choices()))],

            'save_name': rand_str(32),
            'upload_name': f'rainbow{i}',

            'watch_count': random.randint(0, 100),
            'thumb_count': random.randint(0, 100),
            'download_count': random.randint(0, 100),
        }
        photo = Photo.objects.create(**data)
        data['id'] = str(photo.id)
        data['create_time'] = photo.create_time
        data['update_time'] = photo.upload_name
        data_list.append(data)
    return data_list


class PhotoListAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url('PhotoListAPI')
        create_test_data()
        create_test_data()

    def test_get_photo_list(self):
        data = {
            'category': [PhotoTypeEnum.bing, PhotoTypeEnum.anime],
            'offset': 0,
            'count': 10
        }
        resp = self.client.get(self.url, data=data)
        self.assertSuccess(resp)


class PhotoAPIAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url('PhotoAPI')
        self.create_user()

    def test_get_photo(self):
        data_list = create_test_data()
        resp = self.get(self.url, data={'id': data_list[0]['id']})
        self.assertSuccess(resp)

    # def test_post_photo:(self):
    #     in UploadAndDownloadPhotoAPITest

    def test_delete_photo(self):
        data_list = create_test_data()
        ids = [data_list[0]['id'], data_list[1]['id'], data_list[2]['id']]
        resp = self.delete(self.url, data={'ids': ids})
        self.assertSuccess(resp)


class UploadAndDownloadPhotoAPITest(APITestCase):
    def setUp(self):
        self.upload_url = self.get_url('UploadPhotoAPI')
        self.download_url = self.get_url('DownloadPhotoAPI')
        self.createphoto_url = self.get_url('PhotoAPI')

        self.create_user()

    def test_upload_and_download_photo_api(self):
        # 第一步上传图片，获取图片名和图片保存在server的名字
        with tempfile.TemporaryFile() as tmp:
            tmp.write(b'Hello world!')
            tmp.seek(0)
            resp = self.client.post(self.upload_url, data={"file": tmp}, format='multipart')
        self.assertSuccess(resp)
        save_name = resp.data['data']['save_name']
        upload_name = resp.data['data']['upload_name']

        # 创建photo
        data = {
            'name': 'rainbow_test',
            'description': 'rainbow test description',

            'copyright': '©rainbow',
            'category': [PhotoTypeEnum.bing, PhotoTypeEnum.anime],

            'save_name': save_name,
            'upload_name': upload_name
        }
        resp = self.post(self.createphoto_url, data=data)
        self.assertSuccess(resp)
        id = resp.data['data']['id']

        # 下载
        resp = self.post(self.download_url, data={'id': id})
        self.assertSuccess(resp)


class ThumbPhotoAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url('ThumbPhotoAPI')

    def test_add_thumb(self):
        data = create_test_data(1)
        resp = self.post(self.url, {'id': data[0]['id']})
        self.assertSuccess(resp)


class WatchPhotoAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url('WatchPhotoAPI')

    def test_add_watch(self):
        data = create_test_data(1)
        resp = self.post(self.url, {'id': data[0]['id']})
        self.assertSuccess(resp)


# class DownloadGrayPhotoAPITest(APITestCase):
#     def setUp(self):
#         self.url = self.get_url('DownloadGrayPhotoAPI')
#
#     def test_add_watch(self):
#         resp = self.get(self.url)
#         self.assertSuccess(resp)
#         image_base64 = resp.data['data']['image_base64']
#         with open('img.jpg', 'rb') as f:
#             f.write(base64.b64decode(image_base64))
