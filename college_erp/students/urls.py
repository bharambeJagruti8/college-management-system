from django.urls import path
from . import views
from dashboard import views as dashboard_views
from dashboard import views as dashboard_views

urlpatterns = [
# Path ko aise badlo:
path('id-card/', dashboard_views.view_id_card, name='view_id_card'),

path('departments/', views.manage_departments, name='manage_departments'),

# Path ko aise badlo:
path('add-department/', dashboard_views.add_department, name='add_department'),   
path('delete-department/<int:pk>/', views.delete_department, name='delete_department'),

    # Students
path('manage-students/', views.manage_students, name='manage_students'),
path('register/', views.register_student, name='register_student'),  
path('admission/', views.student_admission, name='student_admission'),
path('list/', views.student_list, name='student_list'),
path('edit-student/<int:pk>/', views.edit_student, name='edit_student'),
path('delete-student/<int:pk>/', views.delete_student, name='delete_student'),
path('all-students/', views.student_list_view, name='student_list'),
    

# Path ko aise badlo:
path('id-card/', dashboard_views.view_id_card, name='view_id_card'),
    # Dashboard
path('dashboard/', views.student_dashboard, name='student_dashboard'),
path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

path('logout/', views.logout_view, name='logout'),

path('manage-staff/', views.manage_staff, name='manage_staff'),
path('mark-attendance/', views.mark_attendance, name='mark_attendance'),

path('timetable/', views.student_timetable_view, name='student_timetable'),
path('download-receipt/<int:fee_id>/', views.download_receipt, name='download_receipt'),
path('edit-profile/', views.edit_profile, name='edit_profile') 
]