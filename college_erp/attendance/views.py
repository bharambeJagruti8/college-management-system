from django.shortcuts import render, redirect
from django.contrib import messages
from .models import StudentProfile, Attendance # Apne models ka sahi naam check kar lein
import datetime
from students.models import StudentProfile # ✅ App ka naam use karo

def student_attendance(request):
    # Sabhi students ko database se fetch karna
    students = StudentProfile.objects.all() 
    
    # Ye 'students' variable hi HTML page par names dikhayega
    context = {
        'students': students
    }
    
    return render(request, 'attendance/attendance.html', context)
def attendance_view(request):
    # 1. Sabhi students ko database se nikaalna
    students = StudentProfile.objects.all()

    if request.method == "POST":
        # 2. Form submit hone par attendance save karne ka logic
        for student in students:
            # HTML me radio button ka naam 'status_{{ student.id }}' hai
            status = request.POST.get(f'status_{student.id}')
            
            if status:
                # Attendance record create ya update karna
                Attendance.objects.update_or_create(
                    student=student,
                    date=datetime.date.today(), # Aaj ki date ke liye
                    defaults={'status': status}
                )
        
        messages.success(request, "Attendance successfully saved!")
        return redirect('attendance_page') # Apne URL name ke hisaab se change karein

    # 3. 'students' variable ko HTML template me bhejna
    context = {
        'students': students,
    }
    return render(request, 'attendance.html', context)

def attendance_view(request):
    # 1. Database se students fetch karna
    student_list = StudentProfile.objects.all()
    
    # 2. Context dictionary taiyar karna
    # Yahan 'students' wahi naam hai jo aapne HTML ke loop {% for student in students %} mein use kiya hai
    context = {
        'students': student_list
    }
    
    # 3. Template render karna
    return render(request, 'attendance/attendance.html', context)