from django.shortcuts import render


# Create your views here.
from hrs.models import Dept,Emp


def index(request):
    return render(request, 'index.html', context={})


def depts(request):
    ctx = {'dept_list': Dept.objects.all()}
    return render(request, 'depts.html', context=ctx)


def emps(request):
    dno = int(request.GET['dno'])
    ctx = {'emp_list': Emp.objects.filter(dept_id=dno)}
    return render(request, 'emps.html', context=ctx)

def del_dept(request):
    dno = int(request.GET['dno'])
    if len(Emp.objects.filter(dept_id=dno)):
        ctx = {"res":"部门有员工不能删除"}
        return render(request,'deldepts.html',context=ctx)
    dept = Dept.objects.filter(no=dno)
    dept.delete()
    ctx = {"res": "部门删除成功"}
    return render(request, 'deldepts.html', context=ctx)