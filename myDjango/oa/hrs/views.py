from json import dumps

from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from hrs.models import Dept,Emp


def index(request):
    return render(request, 'index.html', context={})


def depts(request):
    ctx = {'dept_list': Dept.objects.all()}
    return render(request, 'depts.html', context=ctx)


def emps(request,dno):
    # dno = int(request.GET['dno'])
    emp_list = list(Emp.objects.filter(dept_id=dno).select_related('dept'))
    ctx = {'emp_list': emp_list, 'dept_name':emp_list[0].dept.name} if emp_list else {}
    return render(request, 'emps.html', context=ctx)

# def del_dept(request):
#     dno = int(request.GET['dno'])
#     if len(Emp.objects.filter(dept_id=dno)):
#         ctx = {"res":"部门有员工不能删除"}
#         return render(request,'deldepts.html',context=ctx)
#     dept = Dept.objects.filter(no=dno)
#     dept.delete()
#     ctx = {"res": "部门删除成功"}
#     return render(request, 'deldepts.html', context=ctx)


def del_dept(request, dno):
    try:
        Dept.objects.filter(no=dno).delete()
        ctx = {'code':200}
    except:
        ctx = {'code':404}
    # ctx = {"res": "部门删除成功"}
    # 通过redirect()来重定向,请求一个指定页面，reverse取得hrs.urls中地址的名称(name=xxx)
    # return redirect(reverse('depts'))
    return HttpResponse(dumps(ctx),content_type='application/json;charset=utf-8')


class DeptAddForm(forms.Form):
    no = forms.IntegerField(label='部门编号')
    name = forms.CharField(max_length=20,label='部门名称')
    location = forms.CharField(max_length=10,label='部门所在地')



def add(request):
    if request.method == 'GRT':
        f = DeptAddForm()

    else:
        f = DeptAddForm(request.POST)
        if f.is_valid():
            Dept(**f.cleaned_data).save()
            return redirect(reverse('depts'))
        f = DeptAddForm()
    return render(request, 'add.html', {'f': f})