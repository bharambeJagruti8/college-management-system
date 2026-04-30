from django.contrib import admin
from django.urls import path, include
from accounts import views as auth_views
from dashboard import views as dash_views
from attendance.views import student_attendance
from . import views
from students import views as student_views
from accounts import views as acc_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),

    path('', dash_views.admin_dashboard, name='dashboard'),
    path('save-mood/', acc_views.save_mood, name='save_mood'),
    path('admin-dashboard/', dash_views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', student_views.student_dashboard, name='student_dashboard'),

    path('add-student/', auth_views.add_student, name='add_student'),
    path('manage-students/', auth_views.manage_students, name='manage_students'),
    path('add-staff/', auth_views.add_staff, name='add_staff'),
    path('manage-staff/', auth_views.manage_staff, name='manage_staff'),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('search-student/', auth_views.search_student, name='search_student'),

    path('add-department/', auth_views.add_department, name='add_department'),
    path('manage-departments/', auth_views.manage_departments, name='manage_departments'),

    path('Staff/', dash_views.Staff_list, name='Staff_list'),
    path('library/', dash_views.library_dashboard, name='library_dashboard'),
    path('my-id-card/', student_views.view_id_card, name='view_id_card'),

    path('student-attendance/', student_attendance, name='student_attendance'),
    path('attendance/', include('attendance.urls')),
    path('students/', include('students.urls')),
    path('admissions/', include('admissions.urls')),
    path('departments/', include('departments.urls')),
    path('ai/', include('ai_assistant.urls')),
    path('dashboard-module/', include('dashboard.urls')),
    path('staff/', include('staff.urls')),  # staff_dashboard yahan se aayega
    path('bonafide/', include('bonafide.urls')),
    path('doubt-bot/', include('doubt_bot.urls')),
    path('study-roadmap/', include('study_roadmap.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)