from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import datetime
from reportlab.pdfgen import canvas

# Staff app models
from staff.models import StaffProfile as StaffStaffProfile, SyllabusProgress, QuestionBank, LectureSwapRequest, StudentPerformance

# Accounts models
from accounts.models import StaffProfile as AccountStaffProfile, LeaveApplication, Staff

# Dashboard models
from dashboard.models import Timetable, StudentProfile, Attendance, Subject

# Forms
from staff.forms import StaffForm


def manage_staff(request):
    staff_data = Staff.objects.all()
    return render(request, 'dashboard/manage_staff.html', {'staffs': staff_data})


def add_staff(request):
    if request.method == "POST":
        fname = request.POST.get('full_name')
        email = request.POST.get('email')
        desig = request.POST.get('designation')
        mob = request.POST.get('mobile')
        try:
            new_staff = AccountStaffProfile(
                name=fname,
                email=email,
                designation=desig,
                mobile=mob
            )
            new_staff.save()
            messages.success(request, "Staff successfully add ho gaya!")
            return redirect('manage_staff')
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return render(request, 'add_staff.html')


def edit_staff(request, pk):
    staff = get_object_or_404(AccountStaffProfile, pk=pk)
    form = StaffForm(request.POST or None, instance=staff)
    if form.is_valid():
        form.save()
        return redirect('manage_staff')
    return render(request, 'add_staff.html', {'form': form})


def delete_staff(request, pk):
    staff = get_object_or_404(AccountStaffProfile, pk=pk)
    staff.delete()
    return redirect('manage_staff')


@login_required(login_url='/staff/login/')
def staff_dashboard(request):
    user = request.user
    try:
        staff = AccountStaffProfile.objects.get(user=user)
    except AccountStaffProfile.DoesNotExist:
        messages.error(request, 'Staff profile nahi mila!')
        return redirect('login')

    pending_leaves = LeaveApplication.objects.filter(staff=staff, status='Pending').count()
    leave_applications = LeaveApplication.objects.filter(staff=staff).order_by('-applied_on')[:5]
    
    # ✅ Yeh teenon lines change karo
    risk_students = StudentPerformance.objects.none()
    pending_swaps = LectureSwapRequest.objects.none()
    syllabus_list = SyllabusProgress.objects.none()

    context = {
        'staff': staff,
        'today_schedule': [],
        'pending_leaves': pending_leaves,
        'leave_applications': leave_applications,
        'monthly_salary': staff.base_salary,
        'deduction': 0,
        'net_salary': staff.base_salary,
        'risk_students': risk_students,
        'pending_swaps': pending_swaps,
        'syllabus_list': syllabus_list,
    }
    return render(request, 'staff/staff_dashboard.html', context)

@login_required(login_url='/staff/login/')
def staff_timetable(request):
    try:
        import staff.models
        staff_obj = staff.models.StaffProfile.objects.get(user=request.user)
        print(f"Staff found: {staff_obj}")
        timetable = Timetable.objects.filter(staff=staff_obj).order_by('day_of_week', 'start_time')
        print(f"Timetable count: {timetable.count()}")
    except Exception as e:
        print(f"ERROR: {e}")  # ← Yeh print karo
        timetable = []

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    context = {
        'staff': None,
        'timetable': timetable,
        'days': days,
    }
    return render(request, 'staff/staff_timetable.html', context)

@login_required(login_url='/staff/login/')
def staff_students(request):
    staff = get_object_or_404(StaffStaffProfile, user=request.user)
    students = StudentProfile.objects.filter(department__department_name=staff.department)
    context = {
        'staff': staff,
        'students': students,
    }
    return render(request, 'staff/staff_students.html', context)


@login_required(login_url='/staff/login/')
def mark_attendance(request):
    try:
        staff = StaffStaffProfile.objects.get(user=request.user)
    except StaffStaffProfile.DoesNotExist:
        messages.error(request, 'Staff profile nahi mila! Admin se contact karo.')
        return redirect('staff_dashboard')

    students = StudentProfile.objects.filter(department__department_name=staff.department)
    subjects = Subject.objects.filter(assigned_staff=staff)

    if request.method == 'POST':
        date = request.POST.get('date')
        subject_id = request.POST.get('subject')

        if not date:
            messages.error(request, 'Date select karo!')
            return redirect('staff_mark_attendance')
        if not subject_id:
            messages.error(request, 'Subject select karo!')
            return redirect('staff_mark_attendance')

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            messages.error(request, 'Invalid subject!')
            return redirect('staff_mark_attendance')

        for student in students:
            status = request.POST.get(f'attendance_{student.id}', 'False') == 'True'
            Attendance.objects.update_or_create(
                student=student,
                date=date,
                subject=subject,
                defaults={'status': status}
            )

        messages.success(request, 'Attendance saved successfully!')
        return redirect('staff_dashboard')

    context = {
        'staff': staff,
        'students': students,
        'subjects': subjects,
        'today': datetime.date.today(),
    }
    return render(request, 'staff/mark_attendance.html', context)


@login_required(login_url='/staff/login/')
def apply_leave(request):
    acc_staff = get_object_or_404(AccountStaffProfile, user=request.user)

    if request.method == 'POST':
        LeaveApplication.objects.create(
            staff=acc_staff,
            leave_type=request.POST.get('leave_type'),
            from_date=request.POST.get('from_date'),
            to_date=request.POST.get('to_date'),
            reason=request.POST.get('reason'),
        )
        messages.success(request, 'Leave application submitted!')
        return redirect('staff_dashboard')

    context = {'staff': acc_staff}
    return render(request, 'staff/apply_leave.html', context)


def generate_paper(request):
    difficulty = request.GET.get('difficulty', 'Medium')
    questions = QuestionBank.objects.filter(difficulty=difficulty)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Question_Paper_{difficulty}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"EduCore: {difficulty} Exam Paper")
    p.line(100, 790, 500, 790)

    p.setFont("Helvetica", 12)
    y = 750
    for i, q in enumerate(questions, 1):
        p.drawString(100, y, f"Q{i}. {q.question_text} ({q.marks} Marks)")
        y -= 30

    p.showPage()
    p.save()
    return response


def handle_swap(request, swap_id, action):
    swap = LectureSwapRequest.objects.get(id=swap_id)
    if action == 'accept':
        swap.status = 'Accepted'
    else:
        swap.status = 'Rejected'
    swap.save()
    return redirect('staff_dashboard')