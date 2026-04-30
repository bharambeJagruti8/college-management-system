from django.shortcuts import render
from staff.models import StaffProfile
from fees.models import FeeRecord
from results.models import Result
from students.models import StudentProfile
from departments.models import Department 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, get_object_or_404

def dashboard(request):
    
    students_count = StudentProfile.objects.count()
    staff_count = StaffProfile.objects.count()
    department_count = Department.objects.count()

    context = {
        'students_count': students_count,
        'staff_count': staff_count,
        'department_count': department_count
    }

    return render(request, 'home.html', context)

def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(username=u, password=p)

        if user is not None:
            login(request, user)
            # Role-Based Logic
            if role == 'admin' and user.is_superuser:
                return redirect('admin_dashboard')
            elif role == 'student':
                return redirect('student_dashboard')
            else:
                return render(request, 'login.html', {'error': 'Role mismatch!'})
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
            
    return render(request, 'accounts/login.html')

# college_erp/views.py ke andar
def delete_staff(request, staff_id):
    # Aapka staff delete karne ka logic yahan aayega
    return redirect('manage_staff') # Ya jo bhi aapka redirect page 

def mark_attendance(request):
    # Aapka attendance mark karne ka logic yahan aayega
    if request.method == 'POST':
        # logic...
        pass
    return render(request, 'attendance/mark_attendance.html') # Apne template ka path sahi check karo