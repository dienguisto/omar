from django.contrib import admin
from django.conf.urls import url
from . import views
from django.urls import path



app_name = 'contact'

urlpatterns = [
    path('', views.contact , name='contact'),
    path('listing', views.contact_list, name='indexContact'),
    path('<int:contact_id>/', views.contact_detail, name='detailContact'),
    path('delete/<int:contact_id>/', views.contact_delete, name='deleteContact'),
    path('treat/<int:contact_id>/', views.contact_treat, name='treatContact'),
    path('finish/<int:contact_id>/', views.contact_finish, name='finishContact'),

]
