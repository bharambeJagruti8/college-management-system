from django.shortcuts import render
from students.models import StudentProfile
from staff.models import StaffProfile
from fees.models import FeeRecord

def reports_dashboard(request):
    students = StudentProfile.objects.count()
    staff = StaffProfile.objects.count()
    fees = FeeRecord.objects.count()

    context = {
        'students': students,
        'staff': staff,
        'fees': fees
    }

    return render(request, 'reports/dashboard.html', context)

# Create your models here.
