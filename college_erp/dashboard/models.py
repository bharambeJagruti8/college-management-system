from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# 1. Department
class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.department_name

# 2. Student Profile
class StudentProfile(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    marks_10th = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    marks_12th = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    marks_graduation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    course = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    total_classes = models.IntegerField(default=100)
    attended_classes = models.IntegerField(default=0)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    admission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_no})"

# 3. Subject
class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20, unique=True)
    assigned_staff = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.subject_name

# 4. Attendance
# 4. Attendance
class Attendance(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    status = models.BooleanField(default=False)
    # dashboard/models.py mein Attendance model mein yeh add karo
    is_admin_overridden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"
# 5. Timetable
class Timetable(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    staff = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    room_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.subject} - {self.day_of_week}"
# 6. Fee Record  ← sirf ek student field!
class FeeRecord(models.Model):
    student = models.ForeignKey(
        'StudentProfile',
        on_delete=models.CASCADE,
        related_name='dashboard_fees'
    )
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def balance_fees(self):
        return self.total_fees - self.paid_fees

    def __str__(self):
        return f"{self.student} - {self.fee_amount}"

# 7. Grade
class Grade(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()
    grade_point = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade_point}"

# 8. Notification
class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# 9. Bonafide Request
class BonafideRequest(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.status}"

# 10. Notice
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Exam(models.Model):
    subject_name = models.CharField(max_length=100)
    exam_date = models.DateField()
    start_time = models.TimeField()
    duration = models.CharField(max_length=50, default="3 Hours")
    room_no = models.CharField(max_length=20)

    def __clstr__(self):
        return self.subject_name