from django.db import models
from django.db import models
from accounts.models import CustomUser

from students.models import StudentProfile

class Document(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.document_type
# Create your models here.
