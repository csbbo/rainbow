from utils.tests import APITestCase


class GuestBookAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("GuestBookAPI")
        # self.create_user(username='bob', password='123456', login=True)

    def test_leave_message(self):
        resp = self.post(self.url, {'content': 'leave a message...'})
        self.assertSuccess(resp)
