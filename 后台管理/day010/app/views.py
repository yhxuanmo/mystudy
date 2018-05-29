from json import dumps

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from app.models import Grade, Student
from day010.settings import PAGE_NUMBERS

# 引入自定义登录验证装饰器
from app.checkticket import CheckTicket

"""
首页
"""
@CheckTicket
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


"""
头部
"""
@CheckTicket
def head(request):
    if request.method == 'GET':

        return render(request, 'head.html')


"""
左侧
"""
@CheckTicket
def left(request):
    if request.method == 'GET':

        return render(request, 'left.html')



"""
班级列表
"""
@CheckTicket
def grade(request):
    if request.method == 'GET':
        page_num = request.GET.get('page_num', 1)
        grades = Grade.objects.all()
        paginator = Paginator(grades, PAGE_NUMBERS)
        pages = paginator.page(int(page_num))
        return render(request, 'grade.html',{'grades':grades, 'pages':pages})


"""
添加班级
"""
@CheckTicket
def addgrade(request):
    if request.method == 'GET':
        return render(request, 'addgrade.html')
    if request.method == 'POST':
        # 创建班级信息
        g_name = request.POST.get('g_name')
        g = Grade()
        g.g_name = g_name
        g.save()
        return HttpResponseRedirect(reverse('app:grade'))

@CheckTicket
def changegrade(request):
    if request.method == 'GET':
        g_id = request.GET.get('g_id')
        grade = Grade.objects.get(id = g_id)
        return render(request,'addgrade.html',{'grade':grade})
    if request.method == 'POST':
        g_id = request.POST.get('g_id')
        g_name = request.POST.get('g_name')
        grade = Grade.objects.get(id = g_id)
        grade.g_name = g_name
        grade.save()
        return HttpResponseRedirect(reverse('app:grade'))



"""student"""
@CheckTicket
def student(request):
    if request.method=='GET':
        page_num = request.GET.get('page_num', 1)
        students = Student.objects.all()
        paginator = Paginator(students,PAGE_NUMBERS)
        pages = paginator.page(page_num)
        return render(request,'student.html',{'students':students, 'pages':pages})


"""addstu"""
@CheckTicket
def addstu(request):
    if request.method == 'GET':
        grades = Grade.objects.all()
        return render(request,'addstu.html', {'grades':grades})
    if request.method == 'POST':

        s_name = request.POST.get('s_name')
        g_id = request.POST.get('g_id')
        s_img = request.FILES.get('s_img')

        grade = Grade.objects.filter(id=g_id).first()
        Student.objects.create(s_name = s_name, g_id = grade.id, s_img=s_img)
        return HttpResponseRedirect(reverse('app:student'))

@CheckTicket
def delstu(request):
    if request.method == 'GET':
        s_id = request.GET.get('s_id')
        Student.objects.get(id=s_id).delete()
        ctx = {'code':200}
        return HttpResponse(dumps(ctx),content_type='application/json; charset=utf-8')


