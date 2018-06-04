from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from random import choice
from user.models import UserModel, UserTicketModel


def create_ticket():
    s='qwertyuiopasdfghjklzxcvbnm1234567890'
    ticket = ''
    for _ in range(256):
        ticket += choice(s)
    return ticket

def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        username= request.POST.get('username')
        if UserModel.objects.filter(username=username):
            return render(request, 'user/user_register.html', {'u_res':'用户名已存在'})
        email = request.POST.get('email')
        if UserModel.objects.filter(email=email):
            return render(request, 'user/user_register.html', {'e_res':'该邮箱已注册'})
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            return render(request, 'user/user_register.html', {'p_res': '两次输入不一致'})
        icon = request.FILES.get('icon')
        password = make_password(password)
        UserModel.objects.create(username=username, password=password, email=email, icon=icon,)
        return HttpResponseRedirect(reverse('user:login'))


def login(request):
    if request.method=='GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        user = UserModel.objects.filter(username=username).first()
        if not user:
            return render(request, 'user/user_login.html', {'res':'用户名或密码错误'})
        password = request.POST.get('password')
        if not check_password(password, user.password):
            return render(request, 'user/user_login.html', {'res': '用户名或密码错误'})
        ticket = create_ticket()
        out_time = datetime.now() + timedelta(hours=8)
        UserTicketModel.objects.create(user_id=user.id, ticket=ticket, out_time=out_time)
        return HttpResponseRedirect(reverse('home:home'))