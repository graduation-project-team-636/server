from django.test import TestCase, Client
from login.models import User

# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")

    # 1.登录成功
    def test_login_1(self):
        res = self.client.post('/api/login/', {'username': 'test1', 'password': 'test1'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "登录成功")
        