from django.contrib import admin
from .models import CustomUser, Student, Course, Session, Staff, Department, Fee, ExamResult, Attendance, HODProfile, StaffProfile, LeaveApplication

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'course']
    # Student model mein sirf yahi fields hain: name, email, course, profile_pic

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'department']

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'staff_id', 'department']

@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff', 'leave_type', 'status', 'from_date', 'to_date']

@admin.register(HODProfile)
class HODProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'department']

admin.site.register(Course)
admin.site.register(Session)
admin.site.register(Department)
admin.site.register(Fee)
admin.site.register(ExamResult)
admin.site.register(Attendance)