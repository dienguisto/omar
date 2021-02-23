from django.urls import path
from . import views

app_name = 'categorie'

urlpatterns = [
    path('', views.categorie_list, name='indexCategorie'),
    path('create/', views.categorie_create, name='createCategorie'),
    path('<int:categorie_id>/', views.categorie_detail, name='detailCategorie'),
    path('edit/<int:categorie_id>/', views.categorie_edit, name='editCategorie'),
    path('delete/<int:categorie_id>/', views.categorie_delete, name='deleteCategorie'),
]