from django.urls import path
from . import views
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # path('detect',views.detect,name='detect'),
    path('manage',views.index,name='index'),
     url(r'detect', views.detect),
    
]