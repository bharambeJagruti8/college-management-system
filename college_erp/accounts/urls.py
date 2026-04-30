from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('student/home/', views.student_dashboard, name='student_dashboard'),
    path('admin/home/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('save-mood/', views.save_mood, name='save_mood'),
    # accounts/urls.py ya college_erp/urls.py mein dekho
    path('dashboard-redirect/', views.dashboard_redirect, name='dashboard_redirect'),
]