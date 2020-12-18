import copy
import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from account.models import User
from utils.constans import UserTypeEnum
from utils.shortcuts import MyJSONEncoder


class APITestCase(TestCase):
    USERNAME = 'admin'
    PASSWORD = 'admin'

    def get_url(self, url_name):
        return reverse(url_name)

    def create_user(self, username=USERNAME, password=PASSWORD, login=True, user_type=UserTypeEnum.super_admin):
        user = User.object.create(username=username)
        user.set_password(password)
        user.user_type = user_type
        user.save()
        if login:
            self.client.login(username=username, password=password)
        return user

    def assertSuccess(self, response):
        self.assertIsNone(response.data["err"], f"response failed unexpectedly, "
                                                f"response is {json.dumps(response.data, ensure_ascii=False, cls=MyJSONEncoder)}")
        return response.data["data"]

    def assertFailed(self, response, err=None, msg=None, msg__contains=None):  # noqa: N802
        self.assertIsNotNone(response.data["err"], f"response should fail, "
                                                   f"response is {json.dumps(response.data, ensure_ascii=False, cls=MyJSONEncoder)}")
        if err:
            self.assertEqual(response.data["err"], err)
        if msg:
            self.assertEqual(response.data["msg"], msg)
        if msg__contains:
            if isinstance(msg__contains, str):
                self.assertIn(msg__contains, response.data["msg"])
            elif isinstance(msg__contains, list):
                for item in msg__contains:
                    self.assertIn(item, response.data["msg"])
            else:
                raise ValueError()
        return response.data

    def assertDictContains(self, subset, dict_data):  # noqa: N802
        for k in subset.keys():
            self.assertEqual(subset[k], dict_data[k])

    def deepcopy(self, data):
        return copy.deepcopy(data)

    def pprint(self, response, indent=4, ensure_ascii=False):
        data = json.dumps(response.data, indent=indent, ensure_ascii=ensure_ascii, cls=MyJSONEncoder)
        print(data)

    def get(self, path, data=None, follow=False, secure=False, **extra):
        return self.client.get(path, data=data, follow=follow, secure=secure, **extra)

    def post(self, path, data=None, content_type='application/json', follow=False, secure=False, **extra):
        return self.client.post(path, data=data, content_type=content_type, follow=follow, secure=secure, **extra)

    def put(self, path, data='', content_type='application/json', follow=False, secure=False, **extra):
        return self.client.put(path, data=data, content_type=content_type, follow=follow, secure=secure, **extra)

    def delete(self, path, data='', content_type='application/json', follow=False, secure=False, **extra):
        return self.client.delete(path, data=data, content_type=content_type, follow=follow, secure=secure, **extra)
