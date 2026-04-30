from django.shortcuts import render, redirect, get_object_or_404
from .models import Department
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
from django.contrib import messages
@csrf_exempt
def add_department(request):
    if request.method == "POST":
        # HTML form se data uthao
        name = request.POST.get('dept_name')
        code = request.POST.get('dept_code')

        if name and code:
            # Database mein save karo
            Department.objects.create(department_name=name, department_code=code)
            
            # BLACK SCREEN se bachne ke liye ye line zaruri hai:
            return redirect('dashboard') # Aapko wapas dashboard par bhej dega
            
    return render(request, 'departments/manage_department.html')

def manage_department(request):
    if request.method == "POST":
        name = request.POST.get('name')

        if name:
            Department.objects.create(name=name)
            return redirect('manage_department')

    departments = Department.objects.all()
    return render(request, 'departments/manage_department.html', {
        'departments': departments
    })



# 📌 Delete Department
def delete_department(request, pk):
    # Yeh line ID (pk) se us specific MCA entry ko dhoondegi
    dept = get_object_or_404(Department, pk=pk)
    dept.delete() # Database se delete ho jayega
    return redirect('dashboard') # Delete karke wapas dashboard par bhej dega