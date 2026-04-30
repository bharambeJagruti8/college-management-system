from django.urls import path
from . import views

app_name = 'bonafide'

urlpatterns = [
    path('', views.bonafide_index, name='index'),
    path('admin-panel/', views.admin_bonafide, name='admin_bonafide'),
    path('update-status/<int:request_id>/', views.update_status, name='update_status'),
]