from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from home.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods

def home(request):
    """
    首页视图
    """
    if request.method == 'GET':
        wheelList = MainWheel.objects.all()
        navList = MainNav.objects.all()
        mustBuyList = MainMustBuy.objects.all()
        shopList = MainShop.objects.all()
        showList = MainShow.objects.all()
        data = {'wheelList':wheelList,
                'navList': navList,
                'mustBuyList': mustBuyList,
                'shopList': shopList,
                'shopList2to4':shopList[1:3],
                'shopList5to8': shopList[3:7],
                'shopList9to12': shopList[7:],
                'showList': showList,
                'title': '首页'
                }
        return render(request, 'home/home.html', data)


def mine(request):
    if request.method == 'GET':
        return render(request, 'mine/mine.html')


def market(request):
    if request.method == 'GET':
        # 重定向，给url加上默认参数
        return HttpResponseRedirect(reverse('home:user_market', args=('104749', '0', '0')))


def user_market(request, typeid, childid, sortid):
    """
    :param typeid: 分类id
    :param childid: 子分类id
    :param sortid:  排序id
    """
    if request.method == 'GET':
        typeList = FoodType.objects.all()
        if childid == '0':
            goodsList = Goods.objects.filter(categoryid=typeid)
        else:
            goodsList = Goods.objects.filter(categoryid=typeid, childcid=childid)
        foodtypes_current = typeList.filter(typeid=typeid).first()
        if foodtypes_current:
            childtypenames = foodtypes_current.childtypenames.split('#')
            childList = []
            for childtypename in childtypenames:
                childList.append(childtypename.split(':'))

        if sortid == '0':
            pass
        elif sortid == '1':
            goodsList = goodsList.order_by('productnum')
        elif sortid == '2':
            goodsList = goodsList.order_by('-price')
        elif sortid == '3':
            goodsList = goodsList.order_by('price')

        data = {
            'typeList': typeList,
            'goodsList': goodsList,
            'typeid': typeid,
            'childid': childid,
            'childList': childList,
        }
        return render(request, 'market/market.html', data)