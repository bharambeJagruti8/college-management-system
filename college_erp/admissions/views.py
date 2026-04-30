from urllib import request
from django.db.models import Sum
from django.shortcuts import render, redirect
import random
from datetime import date
from decimal import Decimal
from .models import  FeeRecord, Admission
from dashboard.models import StudentProfile, Department
# Baki saare 'from dashboard.models import ...' wali lines HATA DO!
def admission_dashboard(request):
    # 1. Saare students ki list
    students = StudentProfile.objects.all()
    
    # 2. Count nikalo (Yahan variable ka naam dhyan se dekho)
    total_students_count = students.count() 
    
    # 3. Paid Fees ka total
    total_fees_paid = FeeRecord.objects.aggregate(Sum('fee_amount'))['fee_amount__sum'] or 0
    
    # 4. Pending Fees ka logic (Total students * 50000 - Paid)
    expected_total = total_students_count * 50000
    pending_amount = expected_total - total_fees_paid

    context = {
        'students': students,
        'total_students': total_students_count,  # spelling check
        'total_fees': total_fees_paid,
        'pending_fees': pending_amount,          # HTML mein isi naam se bulana
    }
    return render(request, 'admissions/admission_dashboard.html', context)


def student_registration(request):
    all_depts = Department.objects.all()
    
    if request.method == "POST":
        gen_roll = request.POST.get('roll_no') or "STU" + str(random.randint(1000, 9999))
    
    dept_id = request.POST.get('department')
    print(f"DEBUG department id: {dept_id}")  # Terminal mein dekho kya aa raha hai
    
    try:
        dept = Department.objects.get(id=dept_id)
    except Department.DoesNotExist:
        return render(request, 'admissions/admission_form.html', {
            'departments': Department.objects.all(),
            'error': f"Department ID {dept_id} exist nahi karta!"
        })

    StudentProfile.objects.create(
        first_name=request.POST.get('first_name'),
        last_name=request.POST.get('last_name', ''),
        date_of_birth=date(2000, 1, 1),
        email=request.POST.get('email'),
        roll_no=gen_roll,
        mobile_number=request.POST.get('mobile_number'),
        department=dept,
        father_name=request.POST.get('f_name'),
        mother_name=request.POST.get('m_name'),
        aadhar_number=request.POST.get('aadhar'),
        category=request.POST.get('category'),
    )
    return redirect('admissions:admission_dashboard')

    return render(request, 'admissions/admission_form.html', {'departments': all_depts})


from .models import Admission 



def collect_fee(request):

    if request.method == "POST":
        print("POST DATA:", dict(request.POST))

        try:
            sid = request.POST.get('student')
            raw_amount = request.POST.get('amount')   # ✅ match your form field name
            tid = request.POST.get('transaction_id')
            rem = request.POST.get('remarks', '')
            print(f"sid={sid}, amount={raw_amount}, tid={tid}")


            # Validate before saving
            if not sid or not raw_amount or not tid:
                raise ValueError("Student, amount aur transaction ID required hain!")

            amt = Decimal(raw_amount.strip())  # .strip() removes whitespace

            FeeRecord.objects.create(
        student_id=sid,
        fee_amount=amt, 
        transaction_id=tid
    )
            return redirect('admin_dashboard')

        except Exception as e:
            return render(request, 'admissions/collect_fee.html', {
                'error': f"Error: {e}",
                'students': StudentProfile.objects.all()
            })

    return render(request, 'admissions/collect_fee.html', {
        'students': StudentProfile.objects.all()
    })

def pay_fee(request, student_id):
    student = StudentProfile.objects.get(id=student_id)
    
    if request.method == "POST":
        amount = request.POST.get('amount')
        trans_id = request.POST.get('transaction_id')
        
        # Database mein entry create karo
        FeeRecord.objects.create(
            student=student,
            fee_amount=amount,
            transaction_id=trans_id
        )
        # Save hone ke baad wapas dashboard bhej do
        return redirect('/admissions/dashboard/') 

    return render(request, 'admissions/collect_fee.html', {'student': student})