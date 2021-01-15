from django.core.cache import cache

from utils.shortcuts import rand_str
from utils.tests import APITestCase


class LoginAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("LoginAPI")
        self.create_user(username='bob', password='123456', login=False)

    def test_login(self):
        data = {
            'username': 'bob',
            'password': '123456'
        }
        resp = self.post(self.url, data=data)
        self.assertSuccess(resp)


class RegistAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("RegistAPI")

    def test_regist(self):
        captcha = rand_str(length=4, type='lower_hex')
        data = {
            'username': 'bob',
            'password': '123456',
            'email': 'test@test.com',
            'tel': '12345678900',
            'captcha': captcha
        }
        cache.set(data['email'], data['captcha'], timeout=120)
        resp = self.post(self.url, data=data)
        self.assertSuccess(resp)


class AuthInfoAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("AuthInfoAPI")
        self.create_user(username='bob', password='123456', login=True)

    def test_regist(self):
        resp = self.get(self.url)
        self.assertSuccess(resp)
