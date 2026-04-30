import random
import re
from urllib import request
from .forms import StudentAdmissionForm
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password  # Staff password ke liye zaroori
from django.db.models import Sum, Count, Q
from datetime import datetime
from dashboard.models import StudentProfile
# Sahi models import karo (Check your models.py names)
from .models import  Grade,   Staff
from dashboard.models import FeeRecord
from departments.models import Department
from subjects.models import Subject
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from dashboard.models import Timetable
from accounts.models import CustomUser, StaffProfile
from dashboard.models import Attendance
from bonafide.models import BonafideRequest
import datetime

User = get_user_model()

# --- 1. AUTHENTICATION VIEWS ---

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)

        if user is not None:
            login(request, user)
            print(f"DEBUG: User {user.username} logged in. Role is: {user.role}") # Terminal check
            
            # Case-insensitive check (Dhyan se dekho)
            user_role = str(user.role).lower() 
            
            if user.is_superuser or user_role == 'admin':
                print("DEBUG: Redirecting to Admin Dashboard")
                return redirect('admin_dashboard')
            elif user_role == 'student':
                print("DEBUG: Redirecting to Student Dashboard")
                return redirect('student_dashboard')
            else:
                print(f"DEBUG: Role '{user.role}' not matched. Redirecting to Student Dashboard by default.")
                return redirect('student_dashboard')
        else:
            print("DEBUG: Authentication failed.")
            messages.error(request, "Invalid Credentials!")
            
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

# --- 2. STUDENT DASHBOARD ---

@login_required(login_url='login')
def student_dashboard(request):
    try:
        student = StudentProfile.objects.get(admin=request.user)
    except StudentProfile.DoesNotExist:
        return HttpResponse("Student profile nahi mila!")

    # Attendance
    from django.db.models import Sum
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')
    total_c = attendance_records.count()
    total_a = attendance_records.filter(status=True).count()
    overall_perc = round((total_a / total_c * 100), 1) if total_c > 0 else 0

    # Fees
    fee_records = FeeRecord.objects.filter(student=student)
    total_paid = fee_records.aggregate(Sum('fee_amount'))['fee_amount__sum'] or 0
    total_fees = 50000
    f_amount = total_fees - total_paid
    fee_record = fee_records.first()

    context = {
        'student': student,
        'attendance': overall_perc,
        'att_list': attendance_records[:5],
        'attendance_list': attendance_records[:5],
        'present_l': total_a,
        'total_l': total_c,
        'fee_amt': f_amount,
        'fee_obj': fee_record,
        'fee_stat': True if f_amount <= 0 else False,
        'fee_id': getattr(fee_record, 'id', None),
        'today_schedule': [],
    }
    return render(request, 'students/student_dashboard.html', context)

def staff_dashboard(request):
    staff = StaffProfile.objects.get(user=request.user)
    # Baaki data jaise timetable ya leaves hum baad mein fetch karenge
    context = {
        'staff': staff,
        'remaining_leaves': staff.total_leaves - staff.used_leaves,
    }
    return render(request, 'dashboard/staff_dashboard.html', context)

def download_receipt(request, fee_id):
    # Student ki fees ka data uthao
    fee = get_object_or_404(FeeRecord, id=fee_id)
    student = fee.student # Student details nikalne ke liye
    
    context = {
        'fee': fee,
        'student': student,
        'today': datetime.date.today(),
    }
    return render(request, 'students/receipt_pdf.html', context)

def edit_profile(request):
    student = get_object_or_404(StudentProfile, admin=request.user)
    
    if request.method == 'POST':
        # Data fetch karna form se
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')
        
        if request.FILES.get('profile_pic'):
            student.profile_pic = request.FILES.get('profile_pic')
            
        student.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('student_dashboard')
        
    return render(request, 'students/edit_profile.html', {'student': student})

def student_timetable_view(request):
    student = StudentProfile.objects.get(user=request.user)
    
    # 1. Timetable Data (Full Engineering Schedule)
    timetable_data = Timetable.objects.filter(
        department=student.department
    ).order_by('day_of_week', 'start_time')

    # 2. FEES LOGIC (Ye missing tha isliye amount chala jata tha)
    fee_record = FeeRecord.objects.filter(student=student).first()
    fee_str = str(fee_record) if fee_record else "0.00"
    numbers = re.findall(r'\d+\.\d+|\d+', fee_str)
    f_amount = numbers[-1] if numbers else "0.00"
    f_status = getattr(fee_record, 'status', False)

    # 3. Attendance Logic (Taaki sidebar ya cards khali na dikhein)
    total_c = Attendance.objects.filter(student=student).count()
    total_a = Attendance.objects.filter(student=student, status=True).count()
    overall_perc = round((total_a / total_c * 100), 1) if total_c > 0 else 0

    context = {
        'student': student,
        'timetable': timetable_data,
        'fee_amt': f_amount,   # Ab ye chala jayega HTML mein
        'fee_stat': f_status,  # Ab status bhi dikhega
        'attendance': overall_perc,
        'total_l': total_c,
        'present_l': total_a,
    }
    return render(request, 'students/view_timetable.html', context)
    
def register_student(request):
    return HttpResponse("<h1>Main sahi file mein hoon!</h1>")
    if request.method == "POST":
        try:
            dept_id = request.POST.get('department')
            dept_obj = Department.objects.get(id=dept_id)
            
            StudentProfile.objects.create(
                user=request.user,
                roll_no=request.POST.get('roll_no'),
                department_id=dept_id,  # <--- '_id' lagane se Django samajh jayega
                mobile=request.POST.get('mobile'),
                course="MCA"
            )
            messages.success(request, "Registration Successful!")
            return redirect('student_dashboard')
        except Exception as e:
            return render(request, 'students/register_student.html', {'error': str(e), 'departments': Department.objects.all()})

    return render(request, 'students/register_student.html', {'departments': Department.objects.all()})

def student_admission(request):
    # Sabhi departments ko fetch karo dropdown ke liye
    all_depts = Department.objects.all()

    if request.method == "POST":
        # 1. Roll No ka jugaad (Database ki shanti ke liye) ✅
        generated_roll = "STU" + str(random.randint(10000, 99999))

        # 2. Form se Department ki ID uthao
        # Dhyaan dena: HTML mein name="department" hona chahiye
        dept_id = request.POST.get('department') 

        # 3. Student Create karo
        StudentProfile.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            roll_no=generated_roll,
            mobile_number=request.POST.get('mobile_number'),
            email=request.POST.get('email'),
            # Yahan humne department_id set kiya hai ✅
            department_id=dept_id, 
            date_of_birth=request.POST.get('date_of_birth'),
            gender=request.POST.get('gender'),
            category=request.POST.get('category'),
            address=request.POST.get('address') or "N/A"
        )
        return redirect('admin_dashboard')

    # 4. Yahan 'departments' key pass kar rahe hain template ko
    return render(request, 'admissions/admission_form.html', {'departments': all_depts})



def student_list(request):
    students = StudentProfile.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def manage_students(request):
    students = StudentProfile.objects.all()
    return render(request, 'students/manage_students.html', {'students': students})

# students/views.py mein ye function hona chahiye:
def add_department(request):
    if request.method == "POST":
        from departments.models import Department # Local import safety ke liye
        name = request.POST.get('dept_name') 
        code = request.POST.get('dept_code')
        
        if name and code:
            Department.objects.create(name=name, code=code)
            messages.success(request, f"Department '{name}' added successfully!")
            return redirect('manage_departments') 
            
    return render(request, 'departments/manage_department.html')

def add_staff(request):
    if request.method == "POST":
        try:
            new_staff = Staff.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                username=request.POST.get('username'),
                password=make_password(request.POST.get('password')), # Secure password
                staff_type=request.POST.get('staff_type')
            )
            messages.success(request, "Staff member added!")
            return redirect('manage_staff')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return render(request, 'add_staff.html')

def manage_staff(request):
    staff_list = Staff.objects.all()
    return render(request, 'manage_staff.html', {'staff_list': staff_list})

# --- 4. DEPARTMENTS ---

def manage_departments(request):
    departments = Department.objects.all()
    if request.method == "POST":
        name = request.POST.get('dept_name')
        if name:
            Department.objects.create(name=name)
            return redirect('manage_departments')
    return render(request, 'departments/manage_department.html', {'departments': departments})

def delete_department(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    dept.delete()
    messages.success(request, "Department deleted successfully! 🗑️")
    return redirect('manage_departments')

def edit_student(request, pk):
    # Agar tumne StudentProfile use kiya hai toh:
    student = get_object_or_404(StudentProfile, pk=pk)
    
    if request.method == "POST":
        student.roll_no = request.POST.get('roll_no')
        student.mobile = request.POST.get('mobile')
        # Baaki fields jo bhi update karni hain...
        student.save()
        messages.success(request, "Student updated successfully! ✅")
        return redirect('manage_students')
        
    return render(request, 'students/edit_student.html', {'student': student})

def delete_student(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    student.delete()
    messages.success(request, "Student record deleted! 🗑️")
    return redirect('manage_students')

def student_list_view(request):
    # Saare students ko database se fetch kar rahe hain
    students = StudentProfile.objects.all().order_by('-created_at') 
    return render(request, 'students_display.html', {'students': students})

def mark_attendance(request):
    from dashboard.models import StudentProfile, Subject, Attendance
    
    subjects = Subject.objects.all()
    students = StudentProfile.objects.all()

    if request.method == "POST":
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        present_students = request.POST.getlist('attendance') # Checkboxes ka data

        subject = Subject.objects.get(id=subject_id)

        for student in students:
            is_present = str(student.id) in present_students
    
    # Koshish karo sirf keyword arguments use karne ki
    Attendance.objects.create(
        student=student,      # <--- Model field name = object
        subject=subject,      # <--- Model field name = object
        status=is_present     # <--- Model field name = boolean
        # DATE MAT BHEJO YAHAN SE ❌
    )
    return redirect('admin_dashboard')

    return render(request, 'students/mark_attendance.html', {
        'subjects': subjects,
        'students': students
    })
# --- 5. ADMIN DASHBOARD ---

def admin_dashboard(request):
    context = {
        'total_students': StudentProfile.objects.count(),
        'total_departments': Department.objects.count(),
        'total_staff': Staff.objects.count(),
        'recent_admissions': StudentProfile.objects.all().order_by('-id')[:5],
        'bonafide_requests': BonafideRequest.objects.all().order_by('-id'),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

# --- 6. AI CHATBOT LOGIC ---

def ai_chatbot_response(request):
    user_query = request.GET.get('msg', '').lower()
    if "exam" in user_query:
        response = "Exams are coming soon! Check the timetable."
    elif "python" in user_query:
        response = "Python is the best! Use Django for web apps."
    else:
        response = "I am Educore AI. Ask me anything!"
    return JsonResponse({'reply': response})

# students/views.py mein ye hona chahiye:
@login_required(login_url='login')
def view_id_card(request):
    profile = StudentProfile.objects.filter(user=request.user).first()
    return render(request, 'id_card.html', {'profile': profile})