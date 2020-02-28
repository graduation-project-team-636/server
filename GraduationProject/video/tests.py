from django.test import TestCase, Client
from course.models import Course
from login.models import User
from video.models import Video
import os

# Create your tests here.

path = os.path.abspath('.')


class VideoUploadCase(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1", name="test1")
        User.objects.create(username="test2", password="test2", name="test2")
        test1 = User.objects.get(username="test1")
        test1.groupid = 1
        test1.save()
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        with open(path + '\\media\\avatars\\default.png', 'rb+') as fp:
            res = self.client.post(
                '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
        self.client.post('/api/logout/')

    # 1.上传成功
    def test_1(self):
        self.client.post(
            '/api/login/', {'username': 'test1', 'password': 'test1'})
        course_id = Course.objects.get(course_name="aaa").id
        with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
            res = self.client.post(
                '/api/video/upload/', {'course_id': course_id, 'video_name': '1', 'video_duration': 3600, 'video_data': fp})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['error_code'], 0)
        self.assertEqual(res.json()['message'], "上传成功")
        self.assertEqual(len(res.json()['data']), 0)

#     # 2.用户未登录
#     def test_2(self):
#         course_id = Course.objects.get(course_name="aaa").id
#         with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
#             res = self.client.post(
#                 '/api/video/upload/', {'course_id': course_id, 'video_name': '1', 'video_duration': 3600, 'video_data': fp})
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['error_code'], 13)
#         self.assertEqual(res.json()['message'], "用户未登录")
#         self.assertEqual(len(res.json()['data']), 0)

#     # 3.用户不是管理员
#     def test_1(self):
#         self.client.post(
#             '/api/login/', {'username': 'test2', 'password': 'test2'})
#         course_id = Course.objects.get(course_name="aaa").id
#         with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
#             res = self.client.post(
#                 '/api/video/upload/', {'course_id': course_id, 'video_name': '1', 'video_duration': 3600, 'video_data': fp})
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['error_code'], 22)
#         self.assertEqual(res.json()['message'], "用户不是管理员")
#         self.assertEqual(len(res.json()['data']), 0)


# class VideoModifyCase(TestCase):
#     def setUp(self):
#         User.objects.create(username="test1", password="test1", name="test1")
#         User.objects.create(username="test2", password="test2", name="test2")
#         test1 = User.objects.get(username="test1")
#         test1.groupid = 1
#         test1.save()
#         self.client.post(
#             '/api/login/', {'username': 'test1', 'password': 'test1'})
#         with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
#             res = self.client.post(
#                 '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
#         course_id = Course.objects.get(course_name="aaa").id
#         with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
#             res = self.client.post(
#                 '/api/video/upload/', {'course_id': course_id, 'video_name': '1', 'video_duration': 3600, 'video_data': fp})
#         self.client.post('/api/logout/')

#     # 1.修改成功
#     def test_1(self):
#         self.client.post(
#             '/api/login/', {'username': 'test1', 'password': 'test1'})
#         video_id = Video.objects.get(video_name="1").id
#         res = self.client.post(
#             '/api/video/modify/', {'video_id': video_id, 'video_name': '2'})
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['error_code'], 0)
#         self.assertEqual(res.json()['message'], "修改成功")
#         self.assertEqual(res.json()['data']['video_name'], "2")

#     # 2.用户未登录
#     def test_2(self):
#         video_id = Video.objects.get(video_name="1").id
#         res = self.client.post(
#             '/api/video/modify/', {'video_id': video_id, 'video_name': '2'})
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['error_code'], 13)
#         self.assertEqual(res.json()['message'], "用户未登录")
#         self.assertEqual(len(res.json()['data']), 0)

#     # 3.用户不是管理员
#     def test_3(self):
#         self.client.post(
#             '/api/login/', {'username': 'test2', 'password': 'test2'})
#         video_id = Video.objects.get(video_name="1").id
#         res = self.client.post(
#             '/api/video/modify/', {'video_id': video_id, 'video_name': '2'})
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['error_code'], 22)
#         self.assertEqual(res.json()['message'], "用户不是管理员")
#         self.assertEqual(len(res.json()['data']), 0)


# class VideoAccessCase(TestCase):
#     def setUp(self):
#         User.objects.create(username="test1", password="test1", name="test1")
#         User.objects.create(username="test2", password="test2", name="test2")
#         test1 = User.objects.get(username="test1")
#         test1.groupid = 1
#         test1.save()
#         self.client.post(
#             '/api/login/', {'username': 'test1', 'password': 'test1'})
#         with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
#             res = self.client.post(
#                 '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
#         course_id = Course.objects.get(course_name="aaa").id
#         for num in range(1, 4):
#             with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
#                 res = self.client.post(
#                     '/api/video/upload/', {'course_id': course_id, 'video_name': str(num), 'video_duration': 3600, 'video_data': fp})
#         self.client.post('/api/logout/')

#     # 1.获取成功
#     def test_1(self):
#         self.client.post(
#             '/api/login/', {'username': 'test1', 'password': 'test1'})
#         course_id = Course.objects.get(course_name="aaa").id
#         res = self.client.get(
#             '/api/video/access?course_id=' + str(course_id))
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['error_code'], 0)
#         self.assertEqual(res.json()['message'], "获取成功")
#         self.assertEqual(res.json()['data']['video'][0]['video_name'], "1")
#         self.assertEqual(res.json()['data']['video'][1]['video_name'], "2")
#         self.assertEqual(res.json()['data']['video'][2]['video_name'], "3")


# class VideoDeleteCase(TestCase):
#     def setUp(self):
#         User.objects.create(username="test1", password="test1", name="test1")
#         User.objects.create(username="test2", password="test2", name="test2")
#         test1 = User.objects.get(username="test1")
#         test1.groupid = 1
#         test1.save()
#         self.client.post(
#             '/api/login/', {'username': 'test1', 'password': 'test1'})
#         with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
#             res = self.client.post(
#                 '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
#         course_id = Course.objects.get(course_name="aaa").id
#         with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
#             res = self.client.post(
#                 '/api/video/upload/', {'course_id': course_id, 'video_name': '1', 'video_duration': 3600, 'video_data': fp})
#         self.client.post('/api/logout/')

#     # 1.删除成功
#     def test_1(self):
#         self.client.post(
#             '/api/login/', {'username': 'test1', 'password': 'test1'})
#         video_id = Video.objects.get(video_name="1").id
#         res = self.client.post(
#             '/api/video/delete/', {'video_id': video_id})
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['error_code'], 0)
#         self.assertEqual(res.json()['message'], "删除成功")
#         self.assertEqual(len(res.json()['data']), 0)

#     # 2.用户未登录
#     def test_2(self):
#         video_id = Video.objects.get(video_name="1").id
#         res = self.client.post(
#             '/api/video/delete/', {'video_id': video_id})
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['error_code'], 13)
#         self.assertEqual(res.json()['message'], "用户未登录")
#         self.assertEqual(len(res.json()['data']), 0)

#     # 3.用户不是管理员
#     def test_3(self):
#         self.client.post(
#             '/api/login/', {'username': 'test2', 'password': 'test2'})
#         video_id = Video.objects.get(video_name="1").id
#         res = self.client.post(
#             '/api/video/delete/', {'video_id': video_id})
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['error_code'], 22)
#         self.assertEqual(res.json()['message'], "用户不是管理员")
#         self.assertEqual(len(res.json()['data']), 0)


# class VideoQueeyCase(TestCase):
#     def setUp(self):
#         User.objects.create(username="test1", password="test1", name="test1")
#         test1 = User.objects.get(username="test1")
#         test1.groupid = 1
#         test1.save()
#         self.client.post(
#             '/api/login/', {'username': 'test1', 'password': 'test1'})
#         with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
#             res = self.client.post(
#                 '/api/course/create/', {'course_name': 'aaa', 'course_introduction': '本课程面向初级前端工程师', 'course_category': 'fe', 'course_tag': 'vue', 'course_cover': fp})
#         course_id = Course.objects.get(course_name="aaa").id
#         with open("D:\\下载\\k-means.mp4", 'rb+') as fp:
#             res = self.client.post(
#                 '/api/video/upload/', {'course_id': course_id, 'video_name': '1', 'video_duration': 3600, 'video_data': fp})
#         self.client.post('/api/logout/')

#     # 1.获取成功
#     def test_1(self):
#         video_id = Video.objects.get(video_name="1").id
#         res = self.client.get('/api/video/query?video_id=' + str(video_id))
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['error_code'], 0)
#         self.assertEqual(res.json()['message'], "获取成功")
#         self.assertEqual(res.json()['data']['video_id'], video_id)
#         self.assertEqual(res.json()['data']['video_name'], "1")
#         self.assertEqual(res.json()['data']['video_duration'], 3600)
#         self.assertEqual(type(res.json()['data']['video_data']), str)
