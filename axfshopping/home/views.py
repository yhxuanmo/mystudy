from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from home.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, CartModel, OrderModel, OrderGoodsModel
from utils.functions import create_order_num
from user.models import UserTicketModel


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
        user = request.user
        orders = OrderModel.objects.filter(user=user)
        # payed = 0
        # wait_pay = 0
        # for order in orders:
        #     if order.o_status == 0:
        #         wait_pay +=1
        #     elif order.o_status == 1:
        #         payed += 1
        payed = orders.filter(o_status=1).count()
        wait_pay = orders.filter(o_status=0).count()
        data = {'payed': payed, 'wait_pay': wait_pay}
        return render(request, 'mine/mine.html', data)


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
        # 如果购物车已有商品数量，则更新
        ticket = request.COOKIES.get('ticket')
        user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
        if user_ticket:
            user_id = user_ticket.user_id
            goods_in_cart = CartModel.objects.filter(user_id=user_id)
            data['goods_in_cart'] = goods_in_cart
        return render(request, 'market/market.html', data)


# 添加商品
def addcart(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        user = request.user
        data={'code': 200,
              'msg': '请求成功'
              }
        if user.id:
            goods_in_cart = CartModel.objects.filter(user=user,goods_id=goods_id).first()
            if goods_in_cart:
                goods_in_cart.c_num += 1
                data['num'] = goods_in_cart.c_num
                goods_in_cart.save()

            else:
                CartModel.objects.create(user=user, goods_id=goods_id)
                data['num'] = 1
            return JsonResponse(data=data)
        data['code'] = 403
        data['msg'] = '请登录'
        return JsonResponse(data=data)

def subcart(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        user = request.user
        data = {'code': 200,
                'msg' : '请求成功'
                }
        if user.id:
            goods_in_cart = CartModel.objects.filter(user=user,goods_id=goods_id).first()
            if goods_in_cart:
                if goods_in_cart.c_num == 1:
                    goods_in_cart.delete()
                    data['num'] = 0
                else:
                    goods_in_cart.c_num -= 1
                    data['num'] = goods_in_cart.c_num
                    goods_in_cart.save()
                return JsonResponse(data)
            data['num'] = 0
            return JsonResponse(data)
        data['code'] = 403
        data['msg'] = '请登录'
        return JsonResponse(data)


def cart(request):
    if request.method == 'GET':
        user = request.user
        user_cart = CartModel.objects.filter(user=user)
        is_all_select = True
        for info in user_cart:
            if not info.is_select:
                is_all_select = False
        data = {'user_cart':user_cart, 'is_all_select': is_all_select}
        return render(request, 'cart/cart.html', data)


# 改变选中状态
def change_select_status(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        goods_in_cart = CartModel.objects.filter(goods_id=goods_id).first()
        goods_in_cart.is_select = not goods_in_cart.is_select
        goods_in_cart.save()
        data = {'code':200,
                'msg': '请求成功',
                'select_status':goods_in_cart.is_select,
            }
        return JsonResponse(data)

# 全选
def all_select(request):
    if request.method == 'POST':
        user = request.user
        allstatus = request.POST.get('allstatus')
        goods_in_cart = CartModel.objects.filter(user=user, is_select=allstatus)
        for goods_info in goods_in_cart:
            goods_info.is_select = not goods_info.is_select
            goods_info.save()
        if allstatus == 'True':
            allstatus = False
        else:
            allstatus = True
        data = {'code':200, 'msg':'请求成功','allstatus':allstatus}
        return JsonResponse(data)

# 下单
def generate_order(request):
    if request.method == 'GET':
        user = request.user
        user_cart = CartModel.objects.filter(user=user,is_select=True)
        # 如果购物车中有选中的商品才生成订单
        if user_cart:
            o_num = create_order_num()
            # 创建订单
            order = OrderModel.objects.create(user=user, o_num=o_num)
            # 订单中间表中写入数据
            for goods_info in user_cart:
                OrderGoodsModel.objects.create(goods=goods_info.goods, orders=order, goods_num=goods_info.c_num)
            user_cart.delete()
            data = {'order_id':order.id}
            # return render(request, 'order/order_info.html', data)
            return JsonResponse(data)
        data = {'code':9999,
            'msg':'没有选中任何商品'
            }
        # return render(request, 'cart/cart.html', data)
        return JsonResponse(data)


def change_order_status(request):
    """
    改变订单状态
    """
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        user = request.user
        OrderModel.objects.filter(id=order_id,user=user).update(o_status=1)
        return JsonResponse({'code':200, 'msg': '请求成功'})

# 待付款
def wait_pay(request):
    if request.method == 'GET':
        user = request.user
        wait_pay_orders = OrderModel.objects.filter(user=user, o_status=0)
        data = {'wait_pay_orders': wait_pay_orders}
        return render(request, 'order/order_list_wait_pay.html', data)

#  待收货
def payed(request):
    if request.method == 'GET':
        user = request.user
        payed_orders = OrderModel.objects.filter(user=user, o_status=1)
        data = {'payed_orders': payed_orders}
        return render(request, 'order/order_list_payed.html', data)

def wait_pay_to_payed(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        order = OrderModel.objects.filter(id=order_id).first()
        return render(request, 'order/order_info.html', {'order': order})

# 计算总价
def get_total_price(request):
    if request.method == 'GET':
        user = request.user
        user_cart = CartModel.objects.filter(user=user, is_select=True)
        total = 0
        for goods_info in user_cart:
            total += goods_info.goods.price * goods_info.c_num

        data = {'code':200, 'total': total}
        return JsonResponse(data)