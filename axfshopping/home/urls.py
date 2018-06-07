from django.conf.urls import url


from home import views

urlpatterns = [
    # 首页
    url(r'^home/', views.home, name='home'),
    # 个人中心
    url(r'^mine/', views.mine, name='mine'),
    # 闪购
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.user_market, name='user_market'),

    # 添加商品
    url(r'^addcart/', views.addcart, name='addcart'),
    url(r'^subcart/', views.subcart, name='subcart'),

    # 购物车
    url(r'^cart/', views.cart, name='cart'),
    url(r'^changeSelectStatus/', views.change_select_status, name='change_select_status'),
    url(r'^allSelect/', views.all_select, name='all_select'),
    # 购物车中计算总价
    url(r'^getTotalPrice/', views.get_total_price, name='get_total_price'),

    # 下单
    url(r'^generateOrder/', views.generate_order, name='generate_order'),
    # url(r'^orderInfo/',views.order_info, name='order_info'),

    # 改变订单状态
    url(r'^changeOrderStatus/', views.change_order_status, name='change_order_status'),

    # 待支付
    url(r'^waitPay/', views.wait_pay, name='wait_pay'),
    # 待支付
    url(r'^payed/', views.payed, name='payed'),
    # 代付款去支付
    url(r'^waitPayToPayed/', views.wait_pay_to_payed, name='wait_pay_to_payed'),
]
