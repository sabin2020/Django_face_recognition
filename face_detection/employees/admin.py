from django.contrib import admin
from .models import Employee
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    pass
