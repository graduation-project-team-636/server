from course import models
from django.http import JsonResponse
import login
import video
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


def create(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "课程创建成功"
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

        create_form = models.CreateForm(request.POST, request.FILES)
        if create_form.is_valid():  # 获取数据
            course_name = create_form.cleaned_data['course_name']
            course_introduction = create_form.cleaned_data['course_introduction']
            course_category = create_form.cleaned_data['course_category']
            course_tag = create_form.cleaned_data['course_tag']
            course_cover = create_form.cleaned_data['course_cover']

            # 当一切都OK的情况下，创建新的课程
            new_course = models.Course.objects.create(
                course_name=course_name, course_introduction=course_introduction,
                course_category=course_category, course_tag=course_tag,
                course_cover=course_cover)
            # 返回参数
            response['data']['course_id'] = new_course.id
            response['data']['course_name'] = new_course.course_name
            response['data']['course_introduction'] = new_course.course_introduction
            response['data']['course_category'] = new_course.course_category
            response['data']['course_tag'] = new_course.course_tag
            response['data']['course_cover'] = global_settings.BaseUrl + \
                new_course.course_cover.url
            response['data']['course_attendance'] = new_course.course_attendance
            return JsonResponse(response)

    response['message'] = "请求发生错误"
    create_form = models.CreateForm()
    return JsonResponse(response)


def modify(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "课程信息修改成功"
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
        modify_form = models.ModifyForm(request.POST, request.FILES)
        if modify_form.is_valid():  # 获取数据
            course_id = modify_form.cleaned_data['course_id']
            # 查找课程
            try:
                course = models.Course.objects.get(id=course_id)
            except:
                response['error_code'] = 31
                response['message'] = "id不存在"
                return JsonResponse(response)
            # 当一切都OK的情况下，修改课程信息
            course.course_name = modify_form.cleaned_data['course_name']
            course.course_introduction = modify_form.cleaned_data['course_introduction']
            course.course_category = modify_form.cleaned_data['course_category']
            course.course_tag = modify_form.cleaned_data['course_tag']
            # 封面先删除再更新
            course.course_cover.delete()
            course.course_cover = modify_form.cleaned_data['course_cover']
            course.save()

            # 返回参数
            response['data']['course_id'] = course.id
            response['data']['course_name'] = course.course_name
            response['data']['course_introduction'] = course.course_introduction
            response['data']['course_category'] = course.course_category
            response['data']['course_tag'] = course.course_tag
            response['data']['course_cover'] = global_settings.BaseUrl + \
                course.course_cover.url
            response['data']['course_attendance'] = course.course_attendance
            return JsonResponse(response)

    response['message'] = "请求发生错误"
    modify_form = models.CreateForm()
    return JsonResponse(response)


def access(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "获取成功"
    response['data'] = {}
    if request.method == "GET":
        course_category = request.GET.get('course_category')
        course_tag = request.GET.get('course_tag')
        order = int(request.GET.get('order'))
        page = int(request.GET.get('page'))
        # 排序方式，降序
        courses = {}
        if order == 1:
            order = "-create_time"
        elif order == 2:
            order = "-course_attendance"
        if course_category == "all":
            if course_tag == "all":
                courses = models.Course.objects.all().order_by(
                    order)[((page - 1) * 20):((page - 1) * 20 + 19)]
            else:
                courses = models.Course.objects.filter(course_tag=course_tag).order_by(order)[
                    ((page - 1) * 20):((page - 1) * 20 + 19)]
        elif course_tag == "all":
            courses = models.Course.objects.filter(course_category=course_category).order_by(order)[
                ((page - 1) * 20):((page - 1) * 20 + 19)]
        else:
            courses = models.Course.objects.filter(course_category=course_category, course_tag=course_tag).order_by(order)[
                ((page - 1) * 20):((page - 1) * 20 + 19)]
        response['data']['course'] = {}
        tmp_courses = []
        for course in courses:
            tmp_course = {}
            tmp_course['course_id'] = course.id
            tmp_course['course_name'] = course.course_name
            tmp_course['course_introduction'] = course.course_introduction
            tmp_course['course_category'] = course.course_category
            tmp_course['course_tag'] = course.course_tag
            tmp_course['course_cover'] = global_settings.BaseUrl + \
                course.course_cover.url
            tmp_course['course_attendance'] = course.course_attendance
            tmp_courses.append(tmp_course)
        response['data']['course'] = tmp_courses
        return JsonResponse(response)

    response['message'] = "请求发生错误"
    return JsonResponse(response)


def total_num(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "获取成功"
    response['data'] = {}
    if request.method == "GET":
        course_category = request.GET.get('course_category')
        course_tag = request.GET.get('course_tag')
        if course_category == "all":
            if course_tag == "all":
                response['data']['num'] = models.Course.objects.count()
            else:
                response['data']['num'] = models.Course.objects.filter(
                    course_tag=course_tag).count()
        elif course_tag == "all":
            response['data']['num'] = models.Course.objects.filter(
                course_category=course_category).count()
        else:
            response['data']['num'] = models.Course.objects.filter(
                course_category=course_category, course_tag=course_tag).count()

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

        course_id = int(request.POST.get('course_id'))
        try:
            del_course = models.Course.objects.get(id=course_id)
            # 删除所属视频
            video_id = str2list(del_course.video_id)
            for del_video_id in video_id:
                del_video = video.models.Video.objects.get(id=del_video_id)
                # 删除视频文件再删除对象
                del_video.video_data.delete()
                video.models.Video.objects.get(id=del_video_id).delete()
            # 删除参加用户的记录
            course_attendance_id = str2list(del_course.course_attendance_id)
            for del_user_id in course_attendance_id:
                del_user = login.models.User.objects.get(id=del_user_id)
                attendance_course_id = str2list(del_user.attendance_course_id)
                attendance_course_id.remove(course_id)
                del_user.attendance_course_id = list2str(attendance_course_id)
                del_user.save()
            # 删除封面
            del_course.course_cover.delete()
            # 删除课程
            models.Course.objects.get(id=course_id).delete()
        except:
            response['error_code'] = 31
            response['message'] = "id不存在"
            return JsonResponse(response)
        return JsonResponse(response)

    response['message'] = "请求发生错误"
    return JsonResponse(response)


def attend(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "参加成功"
    response['data'] = {}
    if request.method == "POST":
        if not request.session.get('is_login', None):
            response['error_code'] = 13
            response['message'] = "用户未登录"
            return JsonResponse(response)

        course_id = int(request.POST.get('course_id'))
        try:
            course = models.Course.objects.get(id=course_id)
        except:
            response['error_code'] = 31
            response['message'] = "id不存在"
            return JsonResponse(response)

        user = login.models.User.objects.get(id=request.session['user_id'])
        attendance_course_id = str2list(user.attendance_course_id)
        print(course)
        course_attendance_id = str2list(course.course_attendance_id)
        # 记录用户参加课程的id
        if course_id in attendance_course_id:
            # 用户和课程记录同步，以用户记录的信息为准
            if user.id not in course_attendance_id:
                course_attendance_id.append(user.id)
            response['error_code'] = 32
            response['message'] = "已参加过该课程，不能重复参加"
            response['data']['attendance_course_id'] = user.attendance_course_id
            return JsonResponse(response)

        attendance_course_id.append(course_id)
        user.attendance_course_id = list2str(attendance_course_id)
        user.save()
        # 记录参加该课程用户的id
        course_attendance_id.append(user.id)
        course.course_attendance_id = list2str(course_attendance_id)
        course.course_attendance = len(course_attendance_id)
        course.save()
        # 返回参数
        response['data']['attendance_course_id'] = user.attendance_course_id
        return JsonResponse(response)

    response['message'] = "请求发生错误"
    return JsonResponse(response)


def withdraw(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "退出成功"
    response['data'] = {}
    if request.method == "POST":
        if not request.session.get('is_login', None):
            response['error_code'] = 13
            response['message'] = "用户未登录"
            return JsonResponse(response)

        course_id = int(request.POST.get('course_id'))
        try:
            course = models.Course.objects.get(id=course_id)
        except:
            response['error_code'] = 31
            response['message'] = "id不存在"
            return JsonResponse(response)

        user = login.models.User.objects.get(id=request.session['user_id'])
        attendance_course_id = str2list(user.attendance_course_id)
        course_attendance_id = str2list(course.course_attendance_id)
        # 记录用户参加课程的id
        if course_id not in attendance_course_id:
            # 用户和课程记录同步，以用户记录的信息为准
            if user.id in course_attendance_id:
                course_attendance_id.remove(user.id)
            response['error_code'] = 33
            response['message'] = "未参加该课程，不能退出"
            response['data']['attendance_course_id'] = user.attendance_course_id
            return JsonResponse(response)

        attendance_course_id.remove(course_id)
        user.attendance_course_id = list2str(attendance_course_id)
        user.save()
        # 记录参加该课程用户的id
        course_attendance_id.remove(user.id)
        course.course_attendance_id = list2str(course_attendance_id)
        course.course_attendance = len(course_attendance_id)
        course.save()
        # 返回参数
        response['data']['attendance_course_id'] = user.attendance_course_id
        return JsonResponse(response)

    response['message'] = "请求发生错误"
    return JsonResponse(response)


def attended_by_users(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "获取成功"
    response['data'] = {}
    if request.method == "GET":
        if not request.session.get('is_login', None):
            response['error_code'] = 13
            response['message'] = "用户未登录"
            return JsonResponse(response)

        courses = {}
        user = login.models.User.objects.get(id=request.session['user_id'])
        attendance_course_id = str2list(user.attendance_course_id)
        courses = models.Course.objects.filter(id__in=attendance_course_id)
        response['data']['course'] = {}
        tmp_courses = []
        for course in courses:
            tmp_course = {}
            tmp_course['course_id'] = course.id
            tmp_course['course_name'] = course.course_name
            tmp_course['course_introduction'] = course.course_introduction
            tmp_course['course_category'] = course.course_category
            tmp_course['course_tag'] = course.course_tag
            tmp_course['course_cover'] = global_settings.BaseUrl + \
                course.course_cover.url
            tmp_course['course_attendance'] = course.course_attendance
            tmp_courses.append(tmp_course)
        response['data']['course'] = tmp_courses
        return JsonResponse(response)

    response['message'] = "请求发生错误"
    return JsonResponse(response)


def query(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "获取成功"
    response['data'] = {}
    if request.method == "GET":
        course_id = request.GET.get('course_id')
        # 查找id是否存在
        try:
            course = models.Course.objects.get(id=course_id)
        except:
            response['error_code'] = 31
            response['message'] = "id不存在"
            return JsonResponse(response)

        # 返回参数
        response['data']['course_id'] = course.id
        response['data']['course_name'] = course.course_name
        response['data']['course_introduction'] = course.course_introduction
        response['data']['course_category'] = course.course_category
        response['data']['course_tag'] = course.course_tag
        response['data']['course_cover'] = global_settings.BaseUrl + \
            course.course_cover.url
        response['data']['course_attendance'] = course.course_attendance
        return JsonResponse(response)
