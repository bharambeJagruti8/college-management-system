from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_staff, name='manage_staff'),
    path('add/', views.add_staff, name='add_staff'),
    path('delete/<int:pd>/', views.delete_staff, name='delete_staff'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('timetable/', views.staff_timetable, name='staff_timetable'),
    path('students/', views.staff_students, name='staff_students'),
    path('mark-attendance/', views.mark_attendance, name='staff_mark_attendance'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('generate-paper/', views.generate_paper, name='generate_paper'),
    path('handle-swap/<int:swap_id>/<str:action>/', views.handle_swap, name='handle_swap'), # 'name' match hona chahiye
]
