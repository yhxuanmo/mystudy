from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from app import views



urlpatterns = [
    # Django 验证是否登录login_required
    # url(r'^index/', login_required(views.index), name='index'),
    # url(r'^head/',login_required(views.head), name='head'),
    # url(r'^left/', login_required(views.left), name='left'),
    # url(r'^grade/', login_required(views.grade), name='grade'),
    # url(r'^addgrade/', login_required(views.addgrade), name='addgrade'),
    # url(r'^changegrade/', login_required(views.changegrade), name='changegrade'),
    # url(r'^stdent/', login_required(views.student), name='student'),
    # url(r'^addstu/', login_required(views.addstu),name='addstu'),
    # url(r'^delstu/', login_required(views.delstu), name='delstu'),

    url(r'^index/', views.index, name='index'),
    url(r'^head/',views.head, name='head'),
    url(r'^left/', (views.left), name='left'),
    url(r'^grade/', views.grade, name='grade'),
    url(r'^addgrade/', views.addgrade, name='addgrade'),
    url(r'^changegrade/', views.changegrade, name='changegrade'),
    url(r'^stdent/', views.student, name='student'),
    url(r'^addstu/', views.addstu,name='addstu'),
    url(r'^delstu/', views.delstu, name='delstu'),

]