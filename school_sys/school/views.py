from json import dumps

from django.http import HttpResponse
from django.shortcuts import render
from django import forms

from school.models import StudentInfo


# class RegisterForm(forms.Form):
#     name = forms.CharField(max_length=20,label='姓名')
#     passwd = forms.CharField(max_length=20,label='密码')
#     repasswd = forms.CharField(max_length=20,label='重复密码')
#     sex = forms.ChoiceField(label='性别',choices=((1,'男'),(0,'女')),widget=forms.RadioSelect())
#
#     class Meta:
#         model = StudentInfo
#         fields = ('name', 'passwd', 'sex')

def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        res = list(StudentInfo.objects.filter(name=request.POST['uname']))
        print(res)
        if not res:
            ctx = {'error':'用户名或密码错误'}
            return render(request,'login.html',ctx)
        elif request.POST['upwd'] != res[0].passwd:
            ctx = {'error': '用户名或密码错误'}
            return render(request, 'login.html', ctx)
        else:
            return render(request,'res.html',{'res':'登陆成功'})


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    if request.method == 'POST':
        name = request.POST['name']
        passwd = request.POST['passwd']
        sex = request.POST['sex']
        StudentInfo(name=name,passwd=passwd,sex=sex).save()
        return render(request, 'res.html',{'res':'注册成功'})


def find_name(request,name):
    res = StudentInfo.objects.filter(name=name)
    if res:
        ctx = {'here':1}
    else:
        ctx = {'here':0}
    return HttpResponse(dumps(ctx),content_type='application/json;charset=utf-8')