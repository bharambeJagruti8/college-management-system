from django.db import models
from students.models import StudentProfile

class Result(models.Model):
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="exam_results"
    )

    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.student} - {self.subject}"