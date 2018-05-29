import random

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from user.models import Users


# Django自带的登录注册验证
# def register(request):
#     if request.method == 'GET':
#         return render(request,'register.html')
#
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         pwd = request.POST.get('pwd')
#         repwd = request.POST.get('repwd')
#         if not all([username, pwd, repwd]):
#             msg = '请填写完整信息'
#             return render(request,'register.html', {'msg':msg})
#         if pwd != repwd:
#             msg = '两次密码不一致'
#             return render(request, 'register.html', {'msg': msg})
#         User.objects.create_user(username=username, password=pwd)
#
#         return HttpResponseRedirect(reverse('user:login'))
#
# def login(request):
#     if request.method == 'GET':
#         return render(request,'login.html')
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         pwd = request.POST.get('pwd')
#         user = auth.authenticate(username=username,password=pwd)
#         if user:
#             auth.login(request,user)
#             return HttpResponseRedirect(reverse('app:index'))
#         else:
#             msg = '用户名或密码错误'
#             return render(request,'login.html',{'msg':msg})
#
# def logout(request):
#     if request.method == 'GET':
#         auth.logout(request)
#         return HttpResponseRedirect(reverse('user:login'))



def register(request):
    if request.method == 'GET':
        return render(request,'register.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        repwd = request.POST.get('repwd')
        if not all([username, pwd, repwd]):
            msg = '请填写完整信息'
            return render(request,'register.html', {'msg':msg})
        if pwd != repwd:
            msg = '两次密码不一致'
            return render(request, 'register.html', {'msg': msg})
        Users.objects.create(username=username,password=pwd)
        return HttpResponseRedirect(reverse('user:login'))


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = Users.objects.filter(username=username,password=pwd).first()
        if user:
            # 产生随机的字符串，长度28
            s = 'qwertyuiopasdfghjklzxcvbnm0123456789'
            ticket = ''
            for _ in range(28):
                ticket += random.choice(s)
            # 保存在服务端
            user.ticket = ticket
            user.save()
            # 保存在客户端，cookie
            response = HttpResponseRedirect(reverse('app:index'))
            response.set_cookie('ticket',ticket)
            return response
        else:
            msg = '用户名或密码错误'
            return render(request,'login.html',{'msg':msg})


def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect(reverse('user:login'))
        # response = redirect(reverse('user:login'))
        response.delete_cookie('ticket')
        return response
