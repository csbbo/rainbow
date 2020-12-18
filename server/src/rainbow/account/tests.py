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
        data = {
            'username': 'bob',
            'password': '123456',
            'email': 'test@test.com',
            'tel': '12345678900'
        }
        resp = self.post(self.url, data=data)
        self.assertSuccess(resp)

