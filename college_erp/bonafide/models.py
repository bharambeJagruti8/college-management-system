from django.db import models
from django.db import models
from django.conf import settings

class BonafideRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    PURPOSE_CHOICES = [
        ('bank', 'Bank Account Opening'),
        ('visa', 'Visa Application'),
        ('scholarship', 'Scholarship'),
        ('internship', 'Internship'),
        ('other', 'Other'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bonafide_requests'
    )
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    addressed_to = models.CharField(max_length=200)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.purpose} - {self.status}"
# Create your models here.
