from django.db import models
from django.db import models
from accounts.models import CustomUser
from students.models import StudentProfile  # Agar Student wahan hai toh
from dashboard.models import FeeRecord

class FeeRecord(models.Model):
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE)    
    amount = models.IntegerField()
    payment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Paid")

    def __str__(self):
        return self.student.student_name
    
