from video import models
from django.http import JsonResponse
import login
import course
import json
import time
import string
import mimetypes
import static.tools.global_settings as global_settings
from navigation.video import VidToSlides
import os
import threading
import re
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse

# Create your views here.


class PPTExtract(threading.Thread):
    def __init__(self, fileLocation, videoId):
        threading.Thread.__init__(self)
        self.fileLocation = fileLocation
        self.videoId = videoId

    def run(self):
        print("start process video：" + str(self.videoId))
        VidToSlides.main(self.fileLocation, self.videoId)
        video = models.Video.objects.get(id=self.videoId)
        video.extract_down = True
        video.save()
        print("finish process video：" + str(self.videoId))


def list2str(in_list):
    tmp_str = ""
    if len(in_list) == 0:
        return tmp_str
    in_list.sort()
    in_list = [str(x) for x in in_list]
    res = ','.join(in_list)
    return res


def str2list(in_str):
    list = []
    if in_str is None or in_str == '':
        return list
    list = in_str.split(",")
    res = [int(x) for x in list]
    return res


def upload(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "上传成功"
    response['data'] = {}
    if request.method == "POST":
        if not request.session.get('is_login', None):
            response['error_code'] = 13
            response['message'] = "用户未登录"
            return JsonResponse(response)
        user = login.models.User.objects.get(id=request.session['user_id'])
        if user.groupid != 1:
            response['error_code'] = 22
            response['message'] = "用户不是管理员"
            return JsonResponse(response)

        upload_form = models.UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():  # 获取数据
            course_id = upload_form.cleaned_data['course_id']
            video_name = upload_form.cleaned_data['video_name']
            video_duration = upload_form.cleaned_data['video_duration']
            video_data = upload_form.cleaned_data['video_data']
            # 查找课程
            try:
                up_course = course.models.Course.objects.get(id=course_id)
            except:
                response['error_code'] = 31
                response['message'] = "id不存在"
                return JsonResponse(response)
            # 当一切都OK的情况下，上传视频给一个课程

            new_video = models.Video.objects.create(
                video_name=video_name, video_duration=video_duration,
                video_data=video_data)
            # try:
            #     _thread.start_new_thread(VidToSlides.main, (
            #         os.getcwd() + new_video.video_data.url.replace("/", "/"), new_video.id))
            #     new_video.extract_down = True
            #     new_video.save()
            # except:
            #     print("处理ppt失败")
            thread = PPTExtract(
                os.getcwd() + new_video.video_data.url.replace("/", "/"), new_video.id)
            thread.start()
            # 将视频id记录在课程信息中
            video_id = str2list(up_course.video_id)
            video_id.append(new_video.id)
            up_course.video_id = list2str(video_id)
            up_course.save()
            # 返回参数
            response['data']['video_id'] = new_video.id
            response['data']['video_name'] = new_video.video_name
            response['data']['video_duration'] = new_video.video_duration
            response['data']['video_data'] = global_settings.BaseUrl + \
                new_video.video_data.url
            return JsonResponse(response)

    response['message'] = "请求发生错误"
    upload_form = models.UploadForm()
    return JsonResponse(response)


def modify(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "修改成功"
    response['data'] = {}
    if request.method == "POST":
        if not request.session.get('is_login', None):
            response['error_code'] = 13
            response['message'] = "用户未登录"
            return JsonResponse(response)
        user = login.models.User.objects.get(id=request.session['user_id'])
        if user.groupid != 1:
            response['error_code'] = 22
            response['message'] = "用户不是管理员"
            return JsonResponse(response)

        modify_form = models.ModifyForm(request.POST)
        if modify_form.is_valid():  # 获取数据
            video_id = modify_form.cleaned_data['video_id']
            video_name = modify_form.cleaned_data['video_name']
            # 查找视频
            try:
                video = models.Video.objects.get(id=video_id)
            except:
                response['error_code'] = 31
                response['message'] = "id不存在"
                return JsonResponse(response)
            # 当一切都OK的情况下，修改视频信息
            video.video_name = video_name
            video.save()
            # 返回参数
            response['data']['video_id'] = video.id
            response['data']['video_name'] = video.video_name
            response['data']['video_duration'] = video.video_duration
            response['data']['video_data'] = global_settings.BaseUrl + \
                video.video_data.url
            return JsonResponse(response)

    response['message'] = "请求发生错误"
    return JsonResponse(response)


def access(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "获取成功"
    response['data'] = {}
    if request.method == "GET":
        course_id = request.GET.get('course_id')
        # 查找课程
        try:
            ac_course = course.models.Course.objects.get(id=course_id)
        except:
            response['error_code'] = 31
            response['message'] = "id不存在"
            return JsonResponse(response)
        video_id = str2list(ac_course.video_id)
        videos = models.Video.objects.filter(id__in=video_id)
        response['data']['video'] = {}
        tmp_videos = []
        for video in videos:
            tmp_video = {}
            tmp_video['video_id'] = video.id
            tmp_video['video_name'] = video.video_name
            tmp_video['video_duration'] = video.video_duration
            tmp_video['video_data'] = global_settings.BaseUrl + \
                video.video_data.url
            tmp_videos.append(tmp_video)
        response['data']['video'] = tmp_videos
        return JsonResponse(response)

    response['message'] = "请求发生错误"
    return JsonResponse(response)


def delete(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "删除成功"
    response['data'] = {}
    if request.method == "POST":
        if not request.session.get('is_login', None):
            response['error_code'] = 13
            response['message'] = "用户未登录"
            return JsonResponse(response)
        user = login.models.User.objects.get(id=request.session['user_id'])
        if user.groupid != 1:
            response['error_code'] = 22
            response['message'] = "用户不是管理员"
            return JsonResponse(response)

        video_id = int(request.POST.get('video_id'))
        # 查找视频
        try:
            video = models.Video.objects.get(id=video_id)
            # 删除视频文件再删除对象
            video.video_data.delete()
            models.Video.objects.get(id=video_id).delete()
        except:
            response['error_code'] = 31
            response['message'] = "id不存在"
            return JsonResponse(response)
        return JsonResponse(response)

    response['message'] = "请求发生错误"
    return JsonResponse(response)


def query(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "获取成功"
    response['data'] = {}
    if request.method == "GET":
        video_id = request.GET.get('video_id')
        # 查找id是否存在
        try:
            video = models.Video.objects.get(id=video_id)
        except:
            response['error_code'] = 31
            response['message'] = "id不存在"
            return JsonResponse(response)

        # 返回参数
        response['data']['video_id'] = video.id
        response['data']['video_name'] = video.video_name
        response['data']['video_duration'] = video.video_duration
        response['data']['video_data'] = global_settings.BaseUrl + \
            video.video_data.url
        return JsonResponse(response)


def getppt(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "获取成功"
    response['data'] = {}
    if request.method == "GET":
        video_id = request.GET.get('video_id')
        # 查找id是否存在
        try:
            video = models.Video.objects.get(id=video_id)
        except:
            response['error_code'] = 31
            response['message'] = "id不存在"
            return JsonResponse(response)

        if not video.extract_down:
            response['error_code'] = 34
            response['message'] = "暂无ppt图片"
            return JsonResponse(response)
        tmp_ppts = []
        with open(os.getcwd() + "/navigation/video/slides/" + str(video.id) + "/schedule.txt", 'r', encoding='utf-8') as schedule:
            for line in schedule:
                line = line.split()
                tmp_ppt = {}
                tmp_ppt['ppt_positon'] = int(line[1])
                tmp_ppt['ppt_image'] = global_settings.BaseUrl + \
                    "/ppt/" + str(video.id) + "/" + line[0]
                tmp_ppts.append(tmp_ppt)
        # 返回参数
        response['data']['ppt'] = tmp_ppts
        return JsonResponse(response)


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(
                remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data


def stream_video(request):
    """将视频文件以流媒体的方式响应"""
    path = os.getcwd() + request.path.replace('/', '/')
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 8    # 8M 每片,响应体最大体积
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(
            path, offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (
            first_byte, last_byte, size)
    else:
        # 不是以视频流方式的获取时，以生成器方式返回整个文件，节省内存
        resp = StreamingHttpResponse(FileWrapper(
            open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
