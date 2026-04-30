from django.contrib import admin
from django.contrib import admin
from .models import Department
from.models import Student 
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # Match these exactly to your models.py field names
    list_display = ('department_name', 'department_code') 
    list_filter = ('department_name',)
    
admin.site.register(Student)
# Register your models here.
