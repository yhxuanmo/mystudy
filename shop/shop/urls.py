"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from cart import views

urlpatterns = [
    path('',views.index),
    path('add_to_cart/<int:id>', views.add_to_cart),
    path('show_cart', views.show_cart),
    path('del_item/<int:id>', views.del_item),
    path('clear_cart', views.clear_all_item),
    path('admin/', admin.site.urls),
]
