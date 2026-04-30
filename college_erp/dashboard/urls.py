from django.urls import path
from . import views
from dashboard import views as dashboard_views
from dashboard.views import ai_chat
urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),  # ← YEH ADD KAR
    path('get-students/', views.get_students, name='get_students'),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path('admission/', views.student_admission, name='student_admission'),
    path('receipt/<int:student_id>/', views.generate_receipt, name='generate_receipt'),
    path('add-department/', views.add_department, name='add_department'),
    path('delete-department/<int:pk>/', views.delete_department, name='delete_department'),
    path('collect-fee/', views.collect_fee, name='collect_fee'),
    path('student-profile/<str:roll_no>/', views.student_detail, name='student_detail'),
    path('id-card/', dashboard_views.view_id_card, name='view_id_card'),
    path('student/<int:student_id>/', views.student_profile_view, name='student_profile'),
    path('manage-staff/', views.manage_staff, name='manage_staff'),
    path('staff-manage/', views.manage_staff, name='manage_staff'),
    path('add-staff/', views.add_staff, name='add_staff'), # Bina dashboard-module likhe
    path('staff-attendance/', views.staff_attendance, name='staff_attendance'),
    path('mark-attendance/<int:staff_id>/<str:status>/', views.mark_attendance, name='mark_attendance'),
    path('exams-results/', views.exams_results, name='exams_results'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('departments/', views.manage_departments, name='manage_departments'),
    path('timetable/', views.timetable_gen, name='timetable_gen'),
    path('fee-management/', views.fee_management, name='fee_management'),
    path('messaging/', views.messaging, name='messaging'),
    path('logout/', views.user_logout, name='logout'),
    path('attendance-center/', views.attendance_hub, name='attendance_hub'), # Isse upar rakho
    path('edit-staff/<int:id>/', views.edit_staff, name='edit_staff'),
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
    path('ai-chat/', ai_chat, name='ai_chat'),
    path('start-scan/', views.start_attendance_scan, name='start_scan'),
    path('exams/', views.exams_view, name='exams'),
   
]