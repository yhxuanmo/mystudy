from django.shortcuts import render
from home.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow

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
