from django.db import models
# Sahi address ye hai:
from dashboard.models import StudentProfile

class Attendance(models.Model):
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='main_attendance')
    method = models.CharField(max_length=20, default='Face Scan')
    status = models.CharField(
        max_length=10,
        choices=[
            ('Present', 'Present'),
            ('Absent', 'Absent')
        ]
    )

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.status}"