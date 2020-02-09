from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="EmployeeList"),
    path('<int:employee>',views.profile,name="employeeProfile")
    
]