from django.shortcuts import render, redirect
from . import models
from django.http import JsonResponse
import json
import time

# Create your views here.


def index(request):

    return render(request, 'login/index.html')


def login(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "注册成功"
    response['data'] = {}
    # 不允许重复登录
    # if request.session.get('is_login', None):
    #     response['error_code'] = 13
    #     response['message'] = "用户已登录"
    #     return JsonResponse(response)
    if request.method == "POST":
        login_form = models.UserForm(request.POST)
        response['error_code'] = 0
        response['message'] = "登录成功"
        response['data'] = {}
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(username=username)
                if user.password == password:
                        # 登录成功，返回参数
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    response['data']['user_id'] = user.id
                    response['data']['username'] = user.username
                    response['data']['name'] = user.name
                    response['data']['groupid'] = user.groupid
                    response['data']['reg_time'] = user.reg_time.strftime(
                        "%Y-%m-%d %H:%M:%S")
                    response['data']['avatar'] = "http://120.77.146.251:8000" + \
                        user.avatar.url
                    return JsonResponse(response)
                else:
                    response['error_code'] = 12
                    response['message'] = "密码不正确"
            except:
                response['error_code'] = 11
                response['message'] = "用户不存在"
        return JsonResponse(response)

    login_form = models.UserForm()
    return JsonResponse(response)


def register(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "注册成功"
    response['data'] = {}
    # if request.session.get('is_login', None):
    #     response['error_code'] = 22
    #     response['message'] = "登录状态不能注册"
    #     return JsonResponse(response)
    if request.method == "POST":
        register_form = models.RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            name = register_form.cleaned_data['name']

            same_name_user = models.User.objects.filter(username=username)
            if same_name_user:  # 用户名唯一
                response['error_code'] = 21
                response['message'] = '用户已经存在'
                return JsonResponse(response)

            # 当一切都OK的情况下，创建新用户
            new_user = models.User.objects.create(
                username=username, password=password, name=name)
            # 返回参数
            user = models.User.objects.get(username=username)
            response['data']['user_id'] = user.id
            response['data']['username'] = user.username
            response['data']['name'] = user.name
            response['data']['groupid'] = user.groupid
            response['data']['reg_time'] = user.reg_time.strftime("%Y-%m-%d %H:%M:%S")
            response['data']['avatar'] = "http://120.77.146.251:8000" + \
                user.avatar.url
            return JsonResponse(response)

    register_form = models.RegisterForm()
    return JsonResponse(response)


def logout(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "登出成功"
    response['data'] = {}
    if request.method == "POST":
        if not request.session.get('is_login', None):
            response['error_code'] = 13
            response['message'] = "用户未登录"
            return JsonResponse(response)

    request.session.flush()
    return JsonResponse(response)


def profile(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "用户信息获取成功"
    response['data'] = {}
    if request.method == "GET":
        if not request.session.get('is_login', None):
            response['error_code'] = 13
            response['message'] = "用户未登录"
            return JsonResponse(response)
        # 返回用户信息
        user = models.User.objects.get(id=request.session['user_id'])
        response['data']['user_id'] = user.id
        response['data']['username'] = user.username
        response['data']['name'] = user.name
        response['data']['groupid'] = user.groupid
        response['data']['reg_time'] = user.reg_time.strftime("%Y-%m-%d %H:%M:%S")
        response['data']['avatar'] = "http://120.77.146.251:8000" + \
            user.avatar.url
        response['data']['sex'] = user.sex
        response['data']['city'] = user.city
        response['data']['occupation'] = user.occupation
        response['data']['hobby'] = user.hobby
        response['data']['signature'] = user.signature
    return JsonResponse(response)


def profile_update(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "用户信息修改成功"
    response['data'] = {}
    if request.method == "POST":
        if not request.session.get('is_login', None):
            response['error_code'] = 13
            response['message'] = "用户未登录"
            return JsonResponse(response)

        Profile_form = models.ProfileForm(request.POST)
        if Profile_form.is_valid():  # 获取数据
            # 当一切都OK的情况下，更新用户信息
            user = models.User.objects.get(id=request.session['user_id'])
            user.name = Profile_form.cleaned_data['name']
            user.sex = Profile_form.cleaned_data['sex']
            user.city = Profile_form.cleaned_data['city']
            user.occupation = Profile_form.cleaned_data['occupation']
            user.hobby = Profile_form.cleaned_data['hobby']
            user.signature = Profile_form.cleaned_data['signature']
            user.save()

            # 返回参数
            response['data']['user_id'] = user.id
            response['data']['name'] = user.name
            response['data']['sex'] = user.sex
            response['data']['city'] = user.city
            response['data']['occupation'] = user.occupation
            response['data']['hobby'] = user.hobby
            response['data']['signature'] = user.signature
            return JsonResponse(response)

    prifile_form = models.ProfileForm()
    return JsonResponse(response)


def pwd_change(request):

    return JsonResponse(response)


def avatar_change(request):
    response = {}
    response['error_code'] = 0
    response['message'] = "用户头像修改成功"
    response['data'] = {}
    if request.method == "POST":
        if not request.session.get('is_login', None):
            response['error_code'] = 13
            response['message'] = "用户未登录"
            return JsonResponse(response)

        avatar = request.FILES.get("avatar")
        user = models.User.objects.get(id=request.session['user_id'])
        user.avatar = avatar
        user.save()

        # 返回参数
        response['data']['user_id'] = user.id
        response['data']['avatar'] = "http://120.77.146.251:8000" + \
            user.avatar.url

        return JsonResponse(response)

    return JsonResponse(response)

