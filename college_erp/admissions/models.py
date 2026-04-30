from django.db import models
from departments.models import Department
from django.utils import timezone
import uuid



class Student(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="admission_students"
    )

    admission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

# admissions/models.py
class FeeRecord(models.Model):
    # Student se connect kar rahe hain
    student = models.ForeignKey(
        'dashboard.StudentProfile', 
        on_delete=models.CASCADE, 
        related_name='admissions_fees'
    )
    
    # 💰 Fees amount - Default 0 rakha hai taaki Date wala error na aaye
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    # 📅 Ye apne aap aaj ki date lega
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # 🆔 Transaction ID unique honi chahiye
    transaction_id = models.CharField(max_length=100, unique=True)
    
    # 📝 Remarks optional hain
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.first_name} - ₹{self.fee_amount}"

from django.db import models
from dashboard.models import StudentProfile # Student se link karne ke liye

class Admission(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2)
    # Status field abhi mat dalo, pehle ye chalne do
    
    def __str__(self):
        return f"{self.student.first_name} - {self.total_fees}"