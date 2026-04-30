from django.urls import path
from . import views
from .views import add_department

urlpatterns = [
    path('manage/', views.manage_department, name='manage_department'),
    path('add-department/', add_department, name='add_department'),
    path('delete/<int:pk>/', views.delete_department, name='delete_department'),
    path('departments/', views.manage_department, name='manage_department'),
]