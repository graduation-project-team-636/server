from video import models
from django.http import JsonResponse
import login
import course
import json
import time
import string
import static.tools.global_settings as global_settings

# Create your views here.


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
