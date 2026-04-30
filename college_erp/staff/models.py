from django.contrib.auth.models import User
from django.db import models
from django.conf import settings  # <--- Ye import karo
from django.conf import settings
from accounts.models import CustomUser
from students.models import StudentProfile, Subject

class StaffProfile(models.Model):
        user = models.OneToOneField(
        settings.AUTH_USER_MODEL,   # ← change from User or 'auth.User'
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
        staff_id = models.CharField(max_length=100, null=True, blank=True)
        department = models.CharField(max_length=100, null=True, blank=True)
        designation = models.CharField(max_length=100, null=True, blank=True)
        name = models.CharField(max_length=100, null=True, blank=True)
        mobile = models.CharField(max_length=15, null=True, blank=True)
        email = models.EmailField(null=True, blank=True)
        subject_specialization = models.CharField(max_length=100, null=True, blank=True)
        salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
        joining_date = models.DateField(null=True, blank=True)
        leave_count = models.IntegerField(default=0)
        status = models.CharField(max_length=20, default='Active')

        def __str__(self):
            return self.name or "Staff Member"
    
class QuestionBank(models.Model):
    DIFFICULTY_CHOICES = [('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')]
    subject = models.CharField(max_length=100)
    unit = models.IntegerField()
    question_text = models.TextField()
    marks = models.IntegerField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return f"{self.subject} - Q: {self.question_text[:20]}"

# 2. Student Burnout / Risk Predictor Model
class StudentPerformance(models.Model):
    student_name = models.CharField(max_length=100)
    attendance_percentage = models.FloatField()
    avg_marks = models.FloatField()
    is_at_risk = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Yahan automation hai: Agar attendance 75% se kam hai, toh auto-risk!
        if self.attendance_percentage < 75:
            self.is_at_risk = True
        else:
            self.is_at_risk = False
        super().save(*args, **kwargs)

# 3. Smart Lecture Swap Model
class LectureSwapRequest(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')]
    
    # Direct User ki jagah settings.AUTH_USER_MODEL use karo
    from_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_swaps'
    )
    to_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_swaps'
    )
    date = models.DateField()
    subject = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

class Notice(models.Model):
    PRIORITY_CHOICES = [('High', 'High'), ('Normal', 'Normal')]
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Normal')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class SyllabusProgress(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE) 
    subject_name = models.CharField(max_length=100)
    total_units = models.IntegerField(default=5)
    completed_units = models.IntegerField(default=0)
    @property
    def percentage(self):
        if self.total_units > 0:
            return int((self.completed_units / self.total_units) * 100)
        return 0

    def __str__(self):
        return f"{self.subject_name} - {self.percentage}%"