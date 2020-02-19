from django.test import TestCase, Client
from course.models import Course
from login.models import User
import os

# Create your tests here.

path = os.path.abspath('.')


class CourseCreateCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")
        User.objects.create(username="test2", password="test2", name="test2")
        test1 = User.objects.get(username="test1")
        test1.groupid = 1
        test1.save()

    # 1.创建成功
    def test_1(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['error_code'], 0)
            self.assertEqual(res.json()['message'], "课程创建成功")
            self.assertEqual(res.json()['data']['course_name'], "aaa")
            self.assertEqual(
                res.json()['data']['course_introduction'], "本课程面向初级前端工程师")
            self.assertEqual(res.json()['data']['course_category'], "fe")
            self.assertEqual(res.json()['data']['course_tag'], "vue")
            self.assertEqual(
                type(res.json()['data']['course_cover']), str)
            self.assertEqual(res.json()['data']['course_attendance'], 0)

    # 2.用户未登录
    def test_2(self):
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['error_code'], 13)
            self.assertEqual(res.json()['message'], "用户未登录")
            self.assertEqual(len(res.json()['data']), 0)

    # 3.用户不是管理员
    def test_3(self):
        self.client.post(
            '/api/login/', {'username': 'test2', 'password': 'test2'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['error_code'], 22)
            self.assertEqual(res.json()['message'], "用户不是管理员")
            self.assertEqual(len(res.json()['data']), 0)


class CourseModifyCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")
        User.objects.create(username="test2", password="test2", name="test2")
        test1 = User.objects.get(username="test1")
        test1.groupid = 1
        test1.save()

    # 1.修改成功
    def test_1(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            course_id = res.json()['data']['course_id']
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/modify/', {'course_id': course_id, 'course_name': '1', 'course_introduction': '2', 'course_category': '3', 'course_tag': '4', 'course_cover': fp})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['error_code'], 0)
            self.assertEqual(res.json()['message'], "课程信息修改成功")
            self.assertEqual(res.json()['data']['course_name'], "1")
            self.assertEqual(
                res.json()['data']['course_introduction'], "2")
            self.assertEqual(res.json()['data']['course_category'], "3")
            self.assertEqual(res.json()['data']['course_tag'], "4")
            self.assertEqual(
                type(res.json()['data']['course_cover']), str)
            self.assertEqual(res.json()['data']['course_attendance'], 0)

    # 2.用户未登录
    def test_2(self):
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/modify/', {'course_id': 2, 'course_name': '1', 'course_introduction': '2', 'course_category': '3', 'course_tag': '4', 'course_cover': fp})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['error_code'], 13)
            self.assertEqual(res.json()['message'], "用户未登录")
            self.assertEqual(len(res.json()['data']), 0)

    # 3.用户不是管理员
    def test_3(self):
        self.client.post(
            '/api/login/', {'username': 'test2', 'password': 'test2'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/modify/', {'course_id': 2, 'course_name': '1', 'course_introduction': '2', 'course_category': '3', 'course_tag': '4', 'course_cover': fp})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['error_code'], 22)
            self.assertEqual(res.json()['message'], "用户不是管理员")
            self.assertEqual(len(res.json()['data']), 0)

    # 4.id不存在
    def test_4(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/modify/', {'course_id': 2, 'course_name': '1', 'course_introduction': '2', 'course_category': '3', 'course_tag': '4', 'course_cover': fp})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['error_code'], 31)
            self.assertEqual(res.json()['message'], "id不存在")
            self.assertEqual(len(res.json()['data']), 0)


class CourseAccessCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")
        test1 = User.objects.get(username="test1")
        test1.groupid = 1
        test1.save()

    # 1.获取成功
    def test_1(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        for num in range(1, 4):
            with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
                res = self.client.post(
                    '/api/course/create/', {'course_name': str(num), 'course_introduction': str(num), 'course_category': str(num), 'course_tag': str(num), 'course_cover': fp})
        Course.objects.get(course_name='1').course_attendance = 3
        Course.objects.get(course_name='2').course_attendance = 2
        Course.objects.get(course_name='3').course_attendance = 1
        self.client.post('/api/logout/')
        # 标签空的
        res = self.client.get(
            '/api/course/access?course_category=fe&course_tag=all&order=1&page=1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "获取成功")
        self.assertEqual(len(res.json()['data']['course']), 0)
        # 以创建时间排序
        res = self.client.get(
            '/api/course/access?course_category=all&course_tag=all&order=1&page=1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "获取成功")
        self.assertEqual(res.json()['data']['course'][0]['course_name'], "3")
        self.assertEqual(res.json()['data']['course'][1]['course_name'], "2")
        self.assertEqual(res.json()['data']['course'][2]['course_name'], "1")
        # 以参与人数排序
        res = self.client.get(
            '/api/course/access?course_category=all&course_tag=all&order=2&page=1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "获取成功")
        self.assertEqual(res.json()['data']['course'][0]['course_name'], "1")
        self.assertEqual(res.json()['data']['course'][1]['course_name'], "2")
        self.assertEqual(res.json()['data']['course'][2]['course_name'], "3")


class CourseTotalNumCase(TestCase):
    # 1.获取成功
    def test_1(self):
        res = self.client.get(
            '/api/course/total_num?course_category=fe&course_tag=all')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "获取成功")
        self.assertEqual(res.json()['data']['num'], 0)


class CourseDeleteCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")
        User.objects.create(username="test2", password="test2", name="test2")
        test1 = User.objects.get(username="test1")
        test1.groupid = 1
        test1.save()

    # 1.删除成功
    def test_1(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})

            course_id = res.json()['data']['course_id']
        res = self.client.post(
            '/api/course/delete/', {'course_id': course_id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "删除成功")
        self.assertEqual(len(res.json()['data']), 0)

    # 2.用户未登录
    def test_2(self):
        res = self.client.post(
            '/api/course/delete/', {'course_id': 2})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 13)
        self.assertEqual(res.json()['message'], "用户未登录")
        self.assertEqual(len(res.json()['data']), 0)

    # 3.用户不是管理员
    def test_3(self):
        self.client.post(
            '/api/login/', {'username': 'test2', 'password': 'test2'})
        res = self.client.post(
            '/api/course/delete/', {'course_id': 2})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 22)
        self.assertEqual(res.json()['message'], "用户不是管理员")
        self.assertEqual(len(res.json()['data']), 0)

    # 4.id不存在
    def test_4(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        res = self.client.post(
            '/api/course/delete/', {'course_id': 2})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 31)
        self.assertEqual(res.json()['message'], "id不存在")
        self.assertEqual(len(res.json()['data']), 0)


class CourseAttendCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")
        test1 = User.objects.get(username="test1")
        test1.groupid = 1
        test1.save()

    # 1.参加成功
    def test_1(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            course_id = res.json()['data']['course_id']
        res = self.client.post(
            '/api/course/attend/', {'course_id': course_id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "参加成功")
        self.assertEqual(res.json()['data']
                         ['attendance_course_id'], str(course_id))

    # 2.用户未登录
    def test_2(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            course_id = res.json()['data']['course_id']
        self.client.post('/api/logout/')
        res = self.client.post(
            '/api/course/attend/', {'course_id': course_id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 13)
        self.assertEqual(res.json()['message'], "用户未登录")
        self.assertEqual(len(res.json()['data']), 0)

    # 3.已参加过该课程，不能重复参加
    def test_3(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            course_id = res.json()['data']['course_id']
        res = self.client.post(
            '/api/course/attend/', {'course_id': course_id})
        res = self.client.post(
            '/api/course/attend/', {'course_id': course_id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 32)
        self.assertEqual(res.json()['message'], "已参加过该课程，不能重复参加")
        self.assertEqual(res.json()['data']
                         ['attendance_course_id'], str(course_id))

    # 4.id不存在
    def test_4(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        res = self.client.post(
            '/api/course/attend/', {'course_id': 2})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 31)
        self.assertEqual(res.json()['message'], "id不存在")
        self.assertEqual(len(res.json()['data']), 0)


class CourseWithdrawCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")
        test1 = User.objects.get(username="test1")
        test1.groupid = 1
        test1.save()

    # 1.退出成功
    def test_1(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            course_id = res.json()['data']['course_id']
        res = self.client.post(
            '/api/course/attend/', {'course_id': course_id})
        res = self.client.post(
            '/api/course/withdraw/', {'course_id': course_id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "退出成功")
        self.assertEqual(res.json()['data']['attendance_course_id'], "")

    # 2.用户未登录
    def test_2(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            course_id = res.json()['data']['course_id']
        res = self.client.post(
            '/api/course/attend/', {'course_id': course_id})
        self.client.post('/api/logout/')
        res = self.client.post(
            '/api/course/withdraw/', {'course_id': course_id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 13)
        self.assertEqual(res.json()['message'], "用户未登录")
        self.assertEqual(len(res.json()['data']), 0)

    # 3.未参加该课程，不能退出
    def test_3(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})

            course_id = res.json()['data']['course_id']
        res = self.client.post(
            '/api/course/withdraw/', {'course_id': course_id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 33)
        self.assertEqual(res.json()['message'], "未参加该课程，不能退出")
        self.assertEqual(res.json()['data']['attendance_course_id'], "")

    # 4.id不存在
    def test_4(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        res = self.client.post(
            '/api/course/withdraw/', {'course_id': 2})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 31)
        self.assertEqual(res.json()['message'], "id不存在")
        self.assertEqual(len(res.json()['data']), 0)


class CourseAccessByUserCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")
        test1 = User.objects.get(username="test1")
        test1.groupid = 1
        test1.save()

    # 1.获取成功
    def test_1(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            course_id = res.json()['data']['course_id']
        res = self.client.post(
            '/api/course/attend/', {'course_id': course_id})
        res = self.client.get('/api/course/attended_by_users/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "获取成功")
        self.assertEqual(len(res.json()['data']['course']), 1)


    # 2.用户未登录
    def test_2(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            course_id = res.json()['data']['course_id']
        self.client.post('/api/logout/')
        res = self.client.get('/api/course/attended_by_users/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 13)
        self.assertEqual(res.json()['message'], "用户未登录")
        self.assertEqual(len(res.json()['data']), 0)


class CourseQueryCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")
        test1 = User.objects.get(username="test1")
        test1.groupid = 1
        test1.save()

    # 1.获取成功
    def test_1(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
            course_id = res.json()['data']['course_id']
        res = self.client.get('/api/course/query?course_id=' + str(course_id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "获取成功")
        self.assertEqual(res.json()['data']['course_name'], "aaa")
        self.assertEqual(
            res.json()['data']['course_introduction'], "本课程面向初级前端工程师")
        self.assertEqual(res.json()['data']['course_category'], "fe")
        self.assertEqual(res.json()['data']['course_tag'], "vue")
        self.assertEqual(
            type(res.json()['data']['course_cover']), str)
        self.assertEqual(res.json()['data']['course_attendance'], 0)

    # 2.id不存在
    def test_4(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        res = self.client.get('/api/course/query?course_id=11')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 31)
        self.assertEqual(res.json()['message'], "id不存在")
        self.assertEqual(len(res.json()['data']), 0)
