import json
from re import sub
from .models import StudentProfile # Apne model ka naam check karo
from django.db import models
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from httpx import request
from xhtml2pdf import pisa
from dashboard.models import StudentProfile, Department, Attendance,Notice
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from bonafide.models import BonafideRequest
import uuid 
from django.shortcuts import render, get_object_or_404
from accounts.models import CustomUser
from accounts.models import StaffProfile
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from admissions.models import FeeRecord
from decimal import Decimal 
import random
import anthropic

def student_admission(request):
    from .models import Department, StudentProfile
    import uuid

    departments = Department.objects.all()
    print("DEBUG DEPARTMENTS:", departments)

    if request.method == "POST":
        try:
            StudentProfile.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                roll_no="RN" + str(uuid.uuid4())[:6],
                department_id=request.POST.get('department')
            )
            return redirect('admin_dashboard')
        except Exception as e:
            print("ERROR:", e)

    return render(request, 'admissions/admission_form.html', {
        'departments': departments
    })
# 2. PDF Receipt View
def generate_receipt(request, student_id):
    student = StudentProfile.objects.get(id=student_id)
    template_path = 'dashboard/receipt_pdf.html'
    context = {'student': student, 'date': student.admission_date}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Receipt_{student.roll_no}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response

# 3. Main Admin Dashboard (FIXED: Added StudentProfile count here)
def admin_dashboard(request):
    # 1. Saare 4 students yahan se aayenge
    students = StudentProfile.objects.all()
    total_students_count = students.count() # Ye 4 aayega
    
    notices = Notice.objects.all().order_by('-date_posted')[:3]# Latest 3 notices
    monthly_raw = (
        FeeRecord.objects
        .annotate(month=TruncMonth('payment_date'))
        .values('month')
        .annotate(total=Sum('fee_amount'))
        .order_by('month')
    )
    monthly_fee_data = json.dumps([float(entry['total']) for entry in monthly_raw])

    for i, s in enumerate(students):
    # 2. Jo 2 bacchon ne bhari (35k + 20k = 55k)
     total_collected = FeeRecord.objects.aggregate(Sum('fee_amount'))['fee_amount__sum'] or 0
    
    # 3. Expected Total (4 students * 50,000 = 2,00,000)
    # Agar tumhare college ki fees alag hai toh 50000 badal dena
    total_expected = total_students_count * 50000 
    
    # 4. Pending Calculation (2,00,000 - 55,000 = 1,45,000)
    pending_bal = total_expected - total_collected

    notices = Notice.objects.all().order_by('-date_posted')[:3]

    for i, s in enumerate(students):
        s.total_classes = 100
        if i == 0:
            s.attended_classes = 90
        elif i == 1:
            s.attended_classes = 85
        else:
            s.attended_classes = 60
        s.percentage = round((s.attended_classes / s.total_classes) * 100, 2)

    # 75% se kam wale defaulters
    defaulters = [s for s in students if s.percentage < 75]

    total_records = Attendance.objects.count()
    if total_records > 0:
        present_count = Attendance.objects.filter(status=True).count()
        attendance_percentage = (present_count / total_records) * 100
        attendance_display = f"{int(attendance_percentage)}%"
    else:
        attendance_display = "No Records"

    context = {
        'recent_admissions': students,
        'total_students': total_students_count, # Card 1: 4
        'total_revenue': total_collected,       # Card 2: ₹55,000
        'pending_fees': pending_bal,            # Card 3: ₹1,45,000
        'total_staff': 5,
        'total_depts': 2,
        'attendance_display': attendance_display,
        'notices': notices,
        'monthly_fee_data': monthly_fee_data,
        'bonafide_requests': BonafideRequest.objects.all().order_by('-id'), 


}
    return render(request, 'dashboard/admin_dashboard.html', context)


# 4. Add Department
def add_department(request):
    if request.method == "POST":
        dept_name = request.POST.get('dept_name')
        dept_code = request.POST.get('dept_code')
        if dept_name and dept_code:
            Department.objects.create(
                department_name=dept_name,
                department_code=dept_code
            )
            return redirect('manage_departments')
    return redirect('manage_departments')

# 5. Collect Fee - FIXED
def collect_fee(request, student_id=None):
    students = StudentProfile.objects.all()
    selected_student = None
    
    if student_id:
        selected_student = get_object_or_404(StudentProfile, id=student_id)
    
    if request.method == "POST":
        try:
            sid = student_id or request.POST.get('student')
            raw_amount = request.POST.get('amount')
            tid = request.POST.get('transaction_id')

            FeeRecord.objects.create(
                student_id=sid,
                fee_amount=Decimal(raw_amount.strip()),
                transaction_id=tid if tid else f"TXN-{uuid.uuid4().hex[:6].upper()}",
            )
            return redirect('admin_dashboard')

        except Exception as e:
            return render(request, 'admissions/collect_fee.html', {
                'error': f"Error: {e}",
                'students': students,
                'student': selected_student,
            })

    return render(request, 'admissions/collect_fee.html', {
        'students': students,
        'student': selected_student,
    })

def manage_departments(request):
    departments = Department.objects.all()
    return render(request, 'dashboard/manage_department.html', {'departments': departments})

def timetable_gen(request):
    mca_subjects = ['Python', 'DBMS', 'OS', 'Networks', 'AI', 'Web Dev', 'Software Eng']
    eng_subjects = ['Maths', 'Physics', 'C++', 'Electronics', 'Circuits', 'DSA', 'VLSI']

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    import random

    def generate_timetable(subjects):
        timetable = {}
        for day in days:
            random.shuffle(subjects)
            timetable[day] = [
                subjects[0],   # 9-10
                subjects[1],   # 10-11
                'Break',       # 11-11:15
                subjects[2],   # 11:15-12:15
                subjects[3],   # 12:15-1:15
                'Lunch',       # 1:15-2:00
                subjects[4],   # 2-3
                subjects[5],   # 3-4
            ]
        return timetable

    context = {
        'mca_timetable': generate_timetable(mca_subjects),
        'eng_timetable': generate_timetable(eng_subjects),
    }
    return render(request, 'dashboard/timetable_gen.html', context)

def exams_results(request):
    return render(request, 'dashboard/exams_results.html', {}) 

def manage_students(request):
    # Kya tumne ye line likhi hai?
    all_students = StudentProfile.objects.all() 
    
    # Aur kya tumne 'all_students' ko context mein pass kiya hai?
    return render(request, 'students/manage_students.html', {'all_students': all_students})

def fee_management(request):
    fee_records = FeeRecord.objects.all()
    return render(request, 'admissions/collect_fee.html', {'fee_records': fee_records})

def messaging(request):
    return render(request, 'dashboard/messaging.html', {})  # ← banana padega

def attendance_hub(request):
    students = StudentProfile.objects.all()
    staff_members = StaffProfile.objects.all()
    
    for i, s in enumerate(students):
        s.total_classes = 100
        if i == 0:
            s.attended_classes = 90
        elif i == 1:
            s.attended_classes = 85
        else:
            s.attended_classes = 60
        s.percentage = round((s.attended_classes / s.total_classes) * 100, 2)
    
    # 75% se kam wale defaulters
    defaulters = [s for s in students if s.percentage < 75]
    
    return render(request, 'attendance_hub.html', {
        'all_students': students, 
        'all_staff': staff_members,
        'defaulters': defaulters,  # ← yeh add kiya
    })

def delete_department(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    dept.delete()
    return redirect('manage_department')

def edit_staff(request, id):
    # Staff ka data database se uthao
    staff = StaffProfile.objects.get(id=id) 
    return render(request, 'edit_staff.html', {'staff': staff})

def edit_student(request, id):
    student = StudentProfile.objects.get(id=id)
    return render(request, 'edit_student.html', {'student': student})

def user_logout(request):
    logout(request)
    return redirect('login')

def manage_staff(request):
    staffs = StaffProfile.objects.filter(user__role='STAFF')
    return render(request, 'dashboard/manage_staff.html', {'all_staff': staffs})

def add_staff(request):
    if request.method == "POST":
        # Pehle CustomUser banao
        from accounts.models import CustomUser, StaffProfile
        import uuid
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        
        # User create karo
        username = f"staff_{uuid.uuid4().hex[:6]}"
        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            role='STAFF'
        )
        
        # StaffProfile banao
        StaffProfile.objects.create(
            user=user,
            staff_id=f"STF{uuid.uuid4().hex[:4].upper()}",
            department=department,
            designation=designation
        )
        
        return redirect('manage_staff')
    
    return render(request,'add_staff.html')

# 3. Staff Attendance Page (Isko bhi add kar lo taaki baad mein error na aaye)
def staff_attendance(request):
    all_staff = StaffProfile.objects.all() # Ye line add karo taaki staff ki list dikhe
    return render(request, 'staff_attendance.html', {'all_staff': all_staff})

# 6. Staff List
def Staff_list(request):
    faculties = StaffProfile.objects.all()
    depts = Department.objects.all()
    if request.method == "POST":
        StaffProfile.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            department_id=request.POST.get('dept')
        )
        return redirect('Staff_list')
    return render(request, 'Staff_list.html', {'faculties': faculties, 'depts': depts})

# 7. Library Dashboard
def library_dashboard(request):
    books = Book.objects.all()
    if request.method == "POST":
        Book.objects.create(
            title=request.POST.get('title'),
            author=request.POST.get('author'),
            quantity=request.POST.get('qty')
        )
        return redirect('library_dashboard')
    return render(request, 'library.html', {'books': books})

# 8. Student Dashboard View (Cleaned)
@login_required(login_url='login')
def student_dashboard(request):
    try:
        student = StudentProfile.objects.get(admin=request.user)
    except StudentProfile.DoesNotExist:
        return HttpResponse("Student profile nahi mila!")

    # Attendance
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')
    total_c = attendance_records.count()
    total_a = attendance_records.filter(status=True).count()
    overall_perc = round((total_a / total_c * 100), 1) if total_c > 0 else 0

    # Fees
    from django.db.models import Sum
    fee_records = FeeRecord.objects.filter(student=student)
    total_paid = fee_records.aggregate(Sum('fee_amount'))['fee_amount__sum'] or 0
    total_fees = 50000
    f_amount = total_fees - total_paid
    fee_record = fee_records.first()

    context = {
        'student': student,
        'attendance': overall_perc,
        'att_list': attendance_records[:5],
        'present_l': total_a,
        'total_l': total_c,
        'fee_amt': f_amount,
        'fee_obj': fee_record,
        'fee_stat': True if f_amount <= 0 else False,
        'today_schedule': [],
    }
    return render(request, 'students/student_dashboard.html', context)
# 9. AJAX for JSON list
def get_students(request):
    # 'name' field agar StudentProfile mein nahi hai toh ise 'roll_no' kar lo
    students = list(StudentProfile.objects.values(
        'roll_no', 'department__name'
    ).order_by('-id')[:5])
    return JsonResponse({'students': students})

# 1. Sabse upar agar "from .models import StudentProfile" likha hai toh use HATA DO.
from django.shortcuts import render, get_object_or_404

def student_detail(request, student_id):
    # Student ko uski ID se dhoondo, nahi mila toh 404 error
    student = get_object_or_404(StudentProfile, id=student_id)
    
    return render(request, 'dashboard/student_profile.html', {'student': student})

# dashboard/views.py ke sabase niche
@login_required(login_url='login')
def view_id_card(request):
    from .models import StudentProfile  # Local import circular se bachne ke liye
    profile = StudentProfile.objects.filter(user=request.user).first()
    
    if not profile:
        return HttpResponse("Profile not found! Please complete your registration.")
        
    return render(request, 'id_card.html', {'profile': profile})

def admission_dashboard(request):
    students = StudentProfile.objects.all()
    total_students = students.count()
    pending_fees = FeeRecord.objects.filter(payment_status="pending").count()
    completed_fees = FeeRecord.objects.filter(payment_status="paid").count()
    context = {
        "students": students,
        "total_students": total_students,
        "pending_fees": pending_fees,
        "completed_fees": completed_fees
    }
    return render(request, "admissions/dashboard.html", context)

def student_registration(request):
    # 2. Database se saare departments nikaalo ✅
    departments = Department.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        department_id = request.POST.get("department")

        StudentProfile.objects.create(
            name=name,
            email=email,
            phone=phone,
            department_id=department_id
        )
        return redirect("admission_dashboard")

    # 3. Context mein 'departments' ko bhejna mat bhoolna ✅
    context = {
        "departments": departments
    }
    return render(request, "admissions/register_student.html", context)

def student_profile_view(request, student_id):
    # Student ki details ID se nikalna
    student = get_object_or_404(StudentProfile, id=student_id)
    return render(request, 'student_detail.html', {'student': student})

def mark_attendance(request, staff_id, status):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    # Aapke model mein 'status' field hona chahiye jo humne pehle discuss kiya tha
    staff.status = status 
    staff.save()
    return redirect('staff_attendance')

@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        user_message = data.get('message', '')

        client = anthropic.Anthropic(api_key="YOUR_API_KEY_HERE")
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system="Tu EduCore school ERP ka AI assistant hai. Students, fees, attendance, staff ke baare mein help karta hai. Hinglish mein baat kar — friendly aur helpful reh.",
            messages=[{"role": "user", "content": user_message}]
        )
        
        return JsonResponse({'reply': message.content[0].text})
    
    return JsonResponse({'reply': 'Invalid request'})

def start_attendance_scan(request):
    try:
        run_face_scanner() # Upar wala function call karo
        messages.success(request, "Attendance scanning completed successfully!")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('dashboard')

def exams_view(request):
    return render(request, 'exams.html')

from .models import Exam

def exams_view(request):
    if request.method == "POST":
        # Form submission handle karein
        Exam.objects.create(
            subject_name=request.POST.get('subject'),
            exam_date=request.POST.get('date'),
            start_time=request.POST.get('time'),
            room_no=request.POST.get('room')
        )
        return redirect('exams') 

    exams = Exam.objects.all()
    return render(request, 'exams.html', {'exams': exams})