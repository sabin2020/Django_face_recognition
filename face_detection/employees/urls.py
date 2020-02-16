from django.urls import path
from . import views
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns=[
    path('',views.index,name="EmployeeList"),
    path('<int:employee>',views.profile,name="employeeProfile"),
]