from django.core.cache import cache

from management.models import Config
from utils.constans import ConfigEnum
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
        cache.set('captcha_' + data['email'], data['captcha'], timeout=120)
        resp = self.post(self.url, data=data)
        self.assertSuccess(resp)


class AuthInfoAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("AuthInfoAPI")
        self.create_user(username='bob', password='123456', login=True)

    def test_auth_user(self):
        resp = self.get(self.url)
        self.assertSuccess(resp)


class UserAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("UserAPI")
        self.create_user(username='bob', password='123456', login=True)

    def test_user_info(self):
        resp = self.get(self.url)
        self.assertSuccess(resp)

        resp = self.put(self.url, data={'username': 'bob1', 'email': 'bob@raibow.com', 'tel': 12345678901})
        self.assertSuccess(resp)


class EmailCaptchaAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url('EmailCaptchaAPI')

        insert_list = [
            {'key': ConfigEnum.EMAIL_ADDR, 'value': 'admin@foxmail.com'},
            {'key': ConfigEnum.EMAIL_PASSWORD, 'value': 'password'},
            {'key': ConfigEnum.EMAIL_SMTP_SERVER, 'value': 'smtp.qq.com'},
            {'key': ConfigEnum.EMAIL_PORT, 'value': 587},
        ]
        for item in insert_list:
            Config.objects.create(**item)

    def test_get_code(self):
        resp = self.get(self.url, {'email': 'test@gmail.com'})
        # self.assertSuccess(resp)
