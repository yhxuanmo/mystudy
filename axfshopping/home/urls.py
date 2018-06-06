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

    # 下单
    url(r'^generateOrder/', views.generate_order, name='generate_order'),
    # url(r'^orderInfo/',views.order_info, name='order_info'),
]
