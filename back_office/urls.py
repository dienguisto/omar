from django.urls import path

from . import views

app_name = 'back_office'

urlpatterns = [
    path('', views.dashboard, name='home')
]