from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.models import UserModel, UserTicketModel
from utils.functions import create_ticket



def register(request):
    """
    注册
    """
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        # post 请求获取前端提交的数据
        username= request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        icon = request.FILES.get('icon')
        # 判断是否为空
        if not all([username, email, password, icon]):
            return render(request, 'user/user_register.html', {'res': '所有信息不能为空'})
        # 用户名是否存在
        if UserModel.objects.filter(username=username):
            return render(request, 'user/user_register.html', {'u_res':'用户名已存在'})
        # 邮箱是否已存在
        if UserModel.objects.filter(email=email):
            return render(request, 'user/user_register.html', {'e_res':'该邮箱已注册'})
        # 密码是否相等
        if password != password_confirm:
            return render(request, 'user/user_register.html', {'p_res': '两次输入不一致'})
        # 加密密码
        password = make_password(password)
        # 存入数据库  - 创建用户
        UserModel.objects.create(username=username, password=password, email=email, icon=icon,)
        return HttpResponseRedirect(reverse('user:login'))


def login(request):
    """
    登录
    """
    if request.method=='GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        # 查询用户名有效性
        user = UserModel.objects.filter(username=username).first()
        if not user:
            return render(request, 'user/user_login.html', {'res':'用户名或密码错误'})
        password = request.POST.get('password')
        # 验证密码有效性
        if not check_password(password, user.password):
            return render(request, 'user/user_login.html', {'res': '用户名或密码错误'})
        # 生成ticket和过期时间
        ticket = create_ticket()
        out_time = datetime.now() + timedelta(hours=8)
        # ticket存入服务端
        UserTicketModel.objects.create(user_id=user.id, ticket=ticket, out_time=out_time)
        response = HttpResponseRedirect(reverse('home:home'))
        # ticket 存入客户端
        response.set_cookie('ticket', ticket, expires=out_time)
        return response


def logout(request):
    """
    注销
    """
    if request.method == 'GET':
        # 清除cookie中的ticket
        response = HttpResponseRedirect(reverse('user:login'))
        response.delete_cookie('ticket')
        return response