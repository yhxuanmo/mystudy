from django.conf.urls import url

from check import views

urlPatterns = [
    url('showinfo/(?P<carid>[川][A-Z][0-9A-Z]{5})',views.show)
]