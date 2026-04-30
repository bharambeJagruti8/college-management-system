from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_attendance, name='student_attendance'),
    path('attendance/', views.student_attendance, name='attendance'),
    path('mark-attendance/', views.attendance_view, name='mark_attendance'),

]