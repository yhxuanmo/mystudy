from json import dumps

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from check.models import CarInfo


def index(request):
    return render(request,'showinfo.html')


def show(request,carid):
    # try:
    info_list = serializers.serialize('json',CarInfo.objects.filter(car_id=int(carid)))
    ctx = {'info':info_list, 'code':200}
    # except:
    #     ctx = {'code':404}
    return HttpResponse(dumps(ctx), content_type='application/json;charset=utf-8')