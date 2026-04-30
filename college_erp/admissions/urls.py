from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('dashboard/', views.admission_dashboard, name='admission_dashboard'),
    path('register/', views.student_registration, name='student_registration'),
    path('pay-fee/<int:student_id>/', views.pay_fee, name='pay_fee'),
    path('fees/collect/<int:student_id>/', views.pay_fee, name='collect_fee'),
    ]