from django.conf.urls import url
from home import views
urlpatterns = [
    url(r'^home/', views.home, name='home')

]