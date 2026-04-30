from django.db import models
from django.db import models
from accounts.models import CustomUser

class Subject(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StaffSubject(models.Model):
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'STAFF'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('staff', 'subject')
# Create your models here.
