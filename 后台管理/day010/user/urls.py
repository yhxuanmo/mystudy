from django.conf.urls import url

from user import views

urlpatterns = [
    # django自带登录注册
    # url(r'ajregister/', views.register,name='register'),
    # url(r'ajlogin/', views.login, name='login'),
    # url(r'ajlogout/', views.logout, name='logout'),

    # 自己实现的登录注册
    url(r'register/', views.register,name='register'),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
]