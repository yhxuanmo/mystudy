from django.conf.urls import url

from user import views

urlpatterns=[
    # 注册
    url(r'^register/', views.register, name='register'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 注销
    url(r'^logout', views.logout, name='logout'),
]