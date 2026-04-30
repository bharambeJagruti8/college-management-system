from django.db import models
from accounts.models import CustomUser
from django.contrib.auth.models import User
from django.conf import settings
from departments.models import Department
from subjects.models import Subject


CATEGORY_CHOICES = [
    ('OPEN', 'Open'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST'),
]
DAYS = [
    ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday'),
]

class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='student_profile_main')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, default='Male')
    date_of_birth = models.DateField(null=True, blank=True)    
    mobile_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=12, unique=True)
    current_semester = models.IntegerField(default=1)
    total_fees = models.FloatField(default=50000)
    paid_fees = models.FloatField(default=0)
    department = models.ForeignKey('students.Department', on_delete=models.CASCADE)    
    roll_number = models.CharField(max_length=20)
    ai_predicted_grade = models.CharField(max_length=10, default="Analyzing...")
    residential_address = models.TextField(default='')
    current_address = models.TextField(default='')
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    parent_mobile = models.CharField(max_length=15)
    tenth_marks = models.FloatField()
    twelfth_marks = models.FloatField()
    graduation_marks = models.FloatField(default=0.0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='OPEN')
    is_eligible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(
        upload_to='student_faces/', 
        null=True,   # Ye existing rows ko allow karega bina default ke
        blank=True,  # Ye form submit karte waqt photo optional rakhega
        default='student_faces/default_user.png' # (Optional) Ek default image path
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
# students/models.py mein ye add karo (Agar nahi hai toh)

class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    staff_type = models.CharField(max_length=50, choices=[
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
        ('librarian', 'Librarian')
    ])
    profile_pic = models.ImageField(upload_to='staff_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Grade(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    marks = models.IntegerField()
    # Yahan subject field bhi honi chahiye agar tum marks store kar rahi ho
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.marks}"

class BonafideRequest(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    reason = models.TextField(default='')
    status = models.CharField(max_length=20, default='Pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.status}"


class Attendance(models.Model):
    student = models.ForeignKey('dashboard.StudentProfile', on_delete=models.CASCADE, related_name='student_app_attendance')   
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    # Add these fields if you want the percentage property to work
    total_lectures = models.IntegerField(default=0)
    attended_lectures = models.IntegerField(default=0)

    # models.py mein Attendance class ke andar:
def __str__(self):
    # self.date ko string mein badlo (f-string use karo)
    return f"{self.student.first_name} - {self.date}"

class Performance(models.Model):
    student = models.ForeignKey('dashboard.StudentProfile', on_delete=models.CASCADE)  
    internal_score = models.FloatField(default=0)
    assignment_completion = models.FloatField(default=0)
    predicted_sgpa = models.FloatField(null=True, blank=True)

class FeeStatus(models.Model):
    student = models.ForeignKey('dashboard.StudentProfile', on_delete=models.CASCADE)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    receipt_no = models.CharField(max_length=50, blank=True)
    related_name='students_app_feestatus_unique' # <--- Iska naam alag rakho
def __str__(self):
        return f"{self.student.user.username} - {self.is_paid}"

class Timetable(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_time = models.TimeField()
    room_number = models.CharField(max_length=10)
    day_of_week = models.CharField(max_length=10, choices=DAYS) # Fixed choices here

# logic for students/models.py
def attendance_risk(self):
    threshold = 75
    current = (self.attended_lectures / self.total_lectures) * 100
    if current < threshold:
        classes_needed = (threshold * self.total_lectures - 100 * self.attended_lectures) / (100 - threshold)
        return f"Warning! Attend next {int(classes_needed)} classes to reach 75%."
    return "Attendance is safe."

# students/models.py mein Student class ke andar ye functions add karein:

def get_ai_insights(self):
    # Weak Subject Logic
    subjects = {'Python': self.tenth_marks, 'DBMS': self.twelfth_marks, 'Maths': self.graduation_marks}
    weak_subject = min(subjects, key=subjects.get)
    
    # Priority Alert Logic
    if self.tenth_marks < 40 or self.twelfth_marks < 40:
        return f"🚨 Critical: Focus on {weak_subject}. You are at risk in this area!", "danger"
    else:
        return f"✅ Smart Tip: You are doing great! Keep practicing {weak_subject} for 1hr daily.", "info"

def predict_exam_readiness(self):
    # Simple Prediction Algorithm
    readiness = (self.tenth_marks + self.twelfth_marks) / 2
    return round(readiness, 2)

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name