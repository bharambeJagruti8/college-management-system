from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import Staff
from .forms import StaffForm
from .forms import StudentForm
from .models import WellnessTracker # Model import karna mat bhulna
from datetime import datetime
from .models import CustomUser, Student, Course, Session,Staff, Department, Fee, ExamResult, Attendance, HODProfile
from .models import StudentAcademic,StudentGamification, FeeRecord, WellnessTracker
from dashboard.models import StudentProfile, FeeRecord  # FeeStatus ki jagah FeeRecord check karo
from dashboard.models import Timetable
# Role-based redirection
def redirect_dashboard(user):
    print(f"User: {user.username}, Type: {user.user_type}")

    if user.user_type == '1':
        return redirect('/hod-dashboard/')
    elif user.user_type == '2':
        return redirect('/staff-dashboard/')
    elif user.user_type == '3':
        return redirect('/s_dashboard/')
    else:
        return redirect('/admin-dashboard/')


# LOGIN VIEW

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_redirect(request):
    # Role ke basis pe redirection
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'STUDENT':
        return redirect('student_dashboard')
    elif request.user.role == 'STAFF':
        return redirect('staff_dashboard')
    else:
        return redirect('login')
    


def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        # DEBUG - ye sab terminal mein dikhega
        print("=== LOGIN DEBUG ===")
        print(f"Role: {role}")
        print(f"Username: {u}")
        print(f"Password: {p}")
        
        user = authenticate(username=u, password=p)
        print(f"User: {user}")
        
        if user is not None:
            print(f"User role: {user.role}")
            login(request, user)
            if role == 'admin' and user.is_superuser:
                return redirect('admin_dashboard')
            elif role == 'student' and user.role == 'STUDENT':
                return redirect('student_dashboard')
            elif role == 'staff' and user.role == 'STAFF':
                return redirect('staff_dashboard')
            else:
                print(f"ROLE MISMATCH: selected={role}, actual={user.role}")
                return render(request, 'accounts/login.html', {'error': 'Role mismatch!'})
        else:
            print("AUTHENTICATION FAILED")
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials!'})
            
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request) # Ye user ka session khatam kar dega
    return redirect('login')

# In teeno dashboards ke liye alag views
@login_required
def student_dashboard(request):
    academic = StudentAcademic.objects.filter(user=request.user).first()
    game = StudentGamification.objects.filter(user=request.user).first()
    fees = FeeRecord.objects.filter(user=request.user).first()
    moods = WellnessTracker.objects.filter(user=request.user).order_by('-date')[:5]
    today_name = datetime.now().strftime('%a') 
    hour = datetime.now().hour
    greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 17 else "Good Evening"

    student_obj = StudentProfile.objects.filter(user=request.user).first()
    attendance_obj = Attendance.objects.filter(student=student_obj).first() if student_obj else None
    fees_obj = FeeRecord.objects.filter(student=student_obj).first() if student_obj else None
    schedule_qs = Timetable.objects.filter(day=today_name).order_by('start_time')

    
    
    
    context = {
        'academic': academic,
        'student': student_obj if student_obj else {'semester': 3, 'branch': 'MCA'},
        'attendance': attendance_obj if attendance_obj else {'percentage': 85},
        'game': game,
        'fees':  fees_obj if fees_obj else {'pending': 0},
        'moods': moods,
        'greeting':  "HELLO JAGRUTI SYSTEM WORKING",
        'academic': StudentAcademic.objects.filter(user=request.user).first(),
        'schedule': schedule_qs if schedule_qs.exists() else [
            {'subject_name': 'Python Web Dev', 'teacher_name': 'Dr. Sharma', 'start_time': '10:30 AM'},
            {'subject_name': 'Cloud Computing', 'teacher_name': 'Prof. Verma', 'start_time': '02:00 PM'},]
    }
    # Yahan apni wahi file ka naam rakho jo tumne banayi hai
    return render(request, 'students/student_dashboard.html', context)



@login_required
def admin_dashboard(request):
    return render(request, 'dashboards/admin_home.html')

# HOD DASHBOARD
from admissions.models import Student, FeeRecord
from departments.models import Department



# STAFF DASHBOARD

def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')



# GENERAL DASHBOARD
def dashboard(request):
    students = Student.objects.all()
    return render(request, "students/student_dashboard.html", {"students": students})


# MANAGE STAFF

def add_staff(request):
    return render(request, 'add_staff.html')


@login_required
def manage_staff(request):
    return render(request, 'manage_staff.html')


def delete_staff(request, staff_id):

    Staff = get_object_or_404(Staff, id=staff_id)
    Staff.user.delete()
    

    messages.success(request, "Staff deleted!")

    return redirect('manage_staff')

def save_mood(request):
    if request.method == 'POST':
        # Safely get the score
        score_raw = request.POST.get('mood_score', '5') # Default 5 agar kuch na mile
        
        try:
            clean_score = int(score_raw)
            # Yahan hum manually ensure kar rahe hain ki sirf User aur Score jaye
            new_mood = WellnessTracker(
                user=request.user, 
                mood_score=clean_score
            )
            new_mood.save() # objects.create ki jagah .save() use karo
            return redirect('student_dashboard')
        except Exception as e:
            return HttpResponse(f"Dekho yahan error hai: {e}")
            
    return redirect('student_dashboard')
# ADD STUDENT
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_students')
    else:
        form = StudentForm()

    return render(request, 'students/add_student.html', {'form': form})

def manage_students(request):
    return render(request, 'students/manage_students.html')

def add_student_save(request):
    return HttpResponse("SAVE FUNCTION WORKING")


# ADD DEPARTMENT
def add_department(request):
    
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            Department.objects.create(name=name)

        return redirect('add_department')

    return render(request, 'departments/add_department.html')

def add_department_save(request):
    
    if request.method == "POST":
        department_name = request.POST.get('department')

        Department.objects.create(
            name=department_name
        )

        return redirect('departments/add_department.html')
    

def manage_departments(request):
    return render(request, 'departments/manage_departments.html')

def search_student(request):
    return render(request, 'students/search_student.html')

def my_view(request):
    students = Student.objects.all()