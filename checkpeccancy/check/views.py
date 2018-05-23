from json import dumps

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from check.models import CarInfo


def index(request):
    carid='12355'
    info_list = CarInfo.objects.filter(car_id=carid)
    ctx = {'infolist': info_list}
    return render(request,'showinfo.html',ctx)


def show(request,carid):
    try:
        res = CarInfo.objects.filter(car_id=carid)
        info_list =serializers.serialize('json',res)
        ctx = {'infolist':info_list,'code':200}
    except:
        ctx = {'code':404}
    return  HttpResponse(dumps(ctx),content_type='application/json;charset=utf-8')