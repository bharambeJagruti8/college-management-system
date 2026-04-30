from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    ADMIN = 'ADMIN'
    STUDENT = 'STUDENT'
    STAFF = 'STAFF'
    ROLE_CHOICES = [(ADMIN, 'Admin'), (STUDENT, 'Student'), (STAFF, 'Staff')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/', default='default.png')
    bio = models.TextField(max_length=500, blank=True)

class StudentAcademic(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='academic')
    course = models.CharField(max_length=100, default="MCA")
    semester = models.IntegerField(default=1)
    roll_no = models.CharField(max_length=20, unique=True)
    cgpa = models.FloatField(default=0.0)
    attendance_percentage = models.FloatField(default=0.0)
    predicted_result = models.CharField(max_length=100, blank=True, help_text="AI Predicted Grade")

class WellnessTracker(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mood_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    note = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.mood_score}"

class StudentGamification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    streak_count = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

class Badge(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='badges/')
    description = models.TextField()
    students = models.ManyToManyField(CustomUser, related_name='badges')

class FeeRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    @property
    def pending_amount(self):
        return self.total_fees - self.paid_fees

class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class HODProfile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hod_profile")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    def __str__(self):
        return f"HOD: {self.user.username}"

class Staff(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, default='Teacher')
    mobile = models.CharField(max_length=15, default='')
    email = models.EmailField(default='')
    department = models.CharField(max_length=100, default='General')
    subject_specialization = models.CharField(max_length=100, default='General')
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    joining_date = models.DateField(default='2024-01-01')
    leave_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='Active')

class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    course = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='student_faces/', null=True, blank=True)
    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[("Present","Present"),("Absent","Absent")])

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("Paid","Paid"),("Pending","Pending")])

class ExamResult(models.Model):
    date = models.DateField()
    pass_percentage = models.IntegerField()

class Session(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.name

class Departments(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.department_name

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()

# StaffProfile PEHLE define hoga
class StaffProfile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, default='Not Assigned', null=True, blank=True)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_leaves = models.IntegerField(default=24)
    used_leaves = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

# LeaveApplication BAAD MEIN — StaffProfile ke neeche
class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=[
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Emergency Leave', 'Emergency Leave'),
    ])
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    admin_remark = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.staff.user.username} - {self.leave_type} - {self.status}"
    @property
    def total_days(self):
        return (self.to_date - self.from_date).days + 1
    
class StaffTimetable(models.Model):
    staff = models.ForeignKey(
        'accounts.Staff', 
        on_delete=models.CASCADE,
        related_name='account_timetables'  # <--- Add this
    )    
    day = models.CharField(max_length=20, choices=[
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')
    ])
    subject_name = models.CharField(max_length=100) # Iska naam dhyan se dekhna
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, default="Room 101")

    def __str__(self):
        return f"{self.subject_name} ({self.day})"