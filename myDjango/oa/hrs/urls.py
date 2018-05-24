from django.urls import path

from hrs import views

urlpatterns = [
    path('depts', views.depts, name='depts'),
    path('emps/<int:dno>', views.emps, name='emps'),
    path('deldept/<int:dno>', views.del_dept, name='deldept'),
    path('add',views.add)
]
