from django.urls import path
from . import views

app_name = 'doubt_bot'

urlpatterns = [
    path('', views.doubt_bot_index, name='index'),
    path('ask/', views.ask_doubt, name='ask'),
]