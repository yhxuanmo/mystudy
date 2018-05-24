from json import dumps, JSONEncoder

from django.core import serializers
from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from check.models import CarInfo


def index(request):

    return render(request,'showinfo.html')


def show(request,carid):
    try:
        if len(carid) >0 :
            res = CarInfo.objects.filter(car_id__contains=carid)
            info_list =serializers.serialize('json',res)
            ctx = {'infolist':info_list,'code':200}
        else:
            ctx = {'code': 404}
    except:
        ctx = {'code':404}
    return  HttpResponse(dumps(ctx),content_type='application/json;charset=utf-8')


class CarRecordForm(forms.Form):
    car_id = forms.CharField(max_length=7,label='车牌号',error_messages={'max_length':'请输入有效的车牌号'})
    pe_reason = forms.CharField(max_length=100,label='违章原因')
    # pe_date = forms.DateTimeField(label='违章日期')
    punish = forms.CharField(max_length=100,label='处罚方式',required=False)



def add(request):
    if request.method=="GET":
        f = CarRecordForm()
    else:
        f = CarRecordForm(request.POST)
        if f.is_valid():
            CarInfo(**f.cleaned_data).save()
            f = CarRecordForm()
    return render(request,'add.html',{'f':f})



