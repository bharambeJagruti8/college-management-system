from django.urls import path
from . import views

app_name = 'study_roadmap'

urlpatterns = [
    path('', views.roadmap_index, name='index'),
    path('generate/', views.generate_plan, name='generate'),
]