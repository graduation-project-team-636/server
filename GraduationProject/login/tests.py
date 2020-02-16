from django.test import TestCase, Client
from login.models import User
import os

# Create your tests here.

path = os.path.abspath('.')


class UserLoginCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")

    # 1.登录成功
    def test_1(self):
        res = self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "登录成功")
        self.assertEqual(type(res.json()['data']['user_id']), int)
        self.assertEqual(res.json()['data']['username'], "test1")
        self.assertEqual(res.json()['data']['name'], "test1")
        self.assertEqual(res.json()['data']['groupid'], 2)
        self.assertEqual(type(res.json()['data']['reg_time']), str)
        self.assertEqual(type(res.json()['data']['avatar']), str)

    # 2.用户不存在
    def test_2(self):
        res = self.client.post(
            '/api/login/', {'username': 'test2', 'password': 'test2'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 11)
        self.assertEqual(res.json()['message'], "用户不存在")
        self.assertEqual(len(res.json()['data']), 0)

    # 3.密码不正确
    def test_3(self):
        res = self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test2'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 12)
        self.assertEqual(res.json()['message'], "密码不正确")
        self.assertEqual(len(res.json()['data']), 0)


class UserLogoutCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")

    # 1.退出成功
    def test_1(self):
        res = self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        res = self.client.post('/api/logout/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "登出成功")
        self.assertEqual(len(res.json()['data']), 0)

    # 2.用户未登录
    def test_2(self):
        res = self.client.post('/api/logout/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 13)
        self.assertEqual(res.json()['message'], "用户未登录")
        self.assertEqual(len(res.json()['data']), 0)


class UserRegisterCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")

    # 1.注册成功
    def test_1(self):
        res = self.client.post(
            '/api/register/', {'username': 'test2', 'password': 'test2', 'name': 'test2'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "注册成功")
        self.assertEqual(type(res.json()['data']['user_id']), int)
        self.assertEqual(res.json()['data']['username'], "test2")
        self.assertEqual(res.json()['data']['name'], "test2")
        self.assertEqual(res.json()['data']['groupid'], 2)
        self.assertEqual(type(res.json()['data']['reg_time']), str)
        self.assertEqual(type(res.json()['data']['avatar']), str)

    # 2.用户名已存在
    def test_2(self):
        res = self.client.post(
            '/api/register/', {'username': 'test1', 'password': 'test1', 'name': 'tset1'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 21)
        self.assertEqual(res.json()['message'], "用户已经存在")
        self.assertEqual(len(res.json()['data']), 0)


class UserModifyCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")

    # 1.修改成功
    def test_1(self):
        res = self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        res = self.client.post(
            '/api/user/profile/update', {'name': 'test2', 'sex': '1'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "用户信息修改成功")
        self.assertEqual(type(res.json()['data']['user_id']), int)
        self.assertEqual(res.json()['data']['name'], "test2")
        self.assertEqual(res.json()['data']['sex'], "1")
        self.assertEqual(type(res.json()['data']['city']), str)
        self.assertEqual(type(res.json()['data']['occupation']), str)
        self.assertEqual(type(res.json()['data']['hobby']), str)
        self.assertEqual(type(res.json()['data']['signature']), str)

        res = self.client.post(
            '/api/user/profile/update', {'name': 'test1', 'sex': '2',
                                         'city': '广东省 广州市 番禺区', 'occupation': 'java工程师',
                                         'hobby': '健身', 'signature': '个性签名'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "用户信息修改成功")
        self.assertEqual(type(res.json()['data']['user_id']), int)
        self.assertEqual(res.json()['data']['name'], "test1")
        self.assertEqual(res.json()['data']['sex'], "2")
        self.assertEqual(res.json()['data']['city'], '广东省 广州市 番禺区')
        self.assertEqual(res.json()['data']['occupation'], 'java工程师')
        self.assertEqual(res.json()['data']['hobby'], '健身')
        self.assertEqual(res.json()['data']['signature'], '个性签名')

    # 2.用户未登录
    def test_2(self):
        res = self.client.post(
            '/api/user/profile/update', {'name': 'test1', 'sex': '2',
                                         'city': '广东省 广州市 番禺区', 'occupation': 'java工程师',
                                         'hobby': '健身', 'signature': '个性签名'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 13)
        self.assertEqual(res.json()['message'], "用户未登录")
        self.assertEqual(len(res.json()['data']), 0)


class UserAvatarChangeCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")

    # 1.修改成功
    def test_1(self):
        res = self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/user/avatar_change/', {'avatar': fp})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['error_code'], 0)
            self.assertEqual(res.json()['message'], "用户头像修改成功")
            self.assertEqual(type(res.json()['data']['user_id']), int)
            self.assertEqual(type(res.json()['data']['avatar']), str)

    # 2.用户未登录
    def test_2(self):
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/user/avatar_change/', {'avatar': fp})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['error_code'], 13)
            self.assertEqual(res.json()['message'], "用户未登录")
            self.assertEqual(len(res.json()['data']), 0)


class UserProfileCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")

    # 1.获取成功
    def test_1(self):
        res = self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        res = self.client.get('/api/user/profile/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "用户信息获取成功")
        self.assertEqual(type(res.json()['data']['user_id']), int)
        self.assertEqual(res.json()['data']['username'], "test1")
        self.assertEqual(res.json()['data']['name'], "test1")
        self.assertEqual(res.json()['data']['groupid'], 2)
        self.assertEqual(type(res.json()['data']['reg_time']), str)
        self.assertEqual(type(res.json()['data']['avatar']), str)
        self.assertEqual(res.json()['data']['sex'], "1")
        self.assertEqual(res.json()['data']['city'], '')
        self.assertEqual(res.json()['data']['occupation'], '')
        self.assertEqual(res.json()['data']['hobby'], '')
        self.assertEqual(res.json()['data']['signature'], '这个人很懒，什么都没有留下')

    # 2.用户未登录
    def test_2(self):
        res = self.client.get('/api/user/profile/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 13)
        self.assertEqual(res.json()['message'], "用户未登录")
        self.assertEqual(len(res.json()['data']), 0)
