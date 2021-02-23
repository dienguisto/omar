from django.shortcuts import render, redirect


# Create your views here.
from categorie.models import Categorie
from product.models import Produit


def dashboard(request):
    classe_active = 'dashboard'
    produits = Produit.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'back_office/dashboard.html', locals())
