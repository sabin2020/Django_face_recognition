from django.shortcuts import render
from .models import Employee
# Create your views here.
def index(request):
    employees = Employee.objects.all()
    context={
        # 'x':'bimal pan masala'
        'employees':employees    
    }
    return render(request,'employees/EmployeeList.html',context)

def profile(request,employee):
    employeeProfile = Employee.objects.get(id=employee)
    context={
        'pageRoute' : employee,
        'employee' : employeeProfile
    }
    return render(request,'employees/EmployeeProfile.html',context)
