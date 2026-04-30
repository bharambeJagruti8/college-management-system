from django.contrib import admin
from .models import Timetable,FeeRecord,StudentProfile,Department,Subject# Saare models import kar lo

# Agar register nahi hua toh ye forcefully karega

admin.site.register(Timetable)
admin.site.register(FeeRecord)
admin.site.register(StudentProfile)
admin.site.register(Department)
admin.site.register(Subject)
