from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Categorie
from . import forms
from datetime import datetime, date
from django.contrib import messages



# Create your views here.

def categorie_list(request):
    classe_active = 'categorie'
    categories = Categorie.objects.all()

    return render(request, "categorie/categorie_list.html", locals())

def categorie_create(request):
    classe_active = 'categorie'
    if request.method == 'POST':
        form = forms.CreateCategorie(request.POST, request.FILES)
        if form.is_valid():
            # save article to DB # DEBUG: # TODO:
            form.save()
            messages.success(request, "Le catégorie a été créee avec succès !")
            return redirect('categorie:indexCategorie')
    else:
        form = forms.CreateCategorie()
    return render(request, 'categorie/categorie_create.html', {'form': form, 'classe_active': classe_active})


def categorie_detail(request, categorie_id):
	try:
		categorie = Categorie.objects.get(pk=categorie_id)
	except Categorie.DoesNotExist:
		raise Http404("Le categorie n'existe pas")
	return render(request, 'categorie/categorie_detail.html', locals())


def categorie_edit(request, categorie_id):
    classe_active = 'categorie'
    post = get_object_or_404(Categorie, pk=categorie_id)
    if request.method == 'POST':
        form = forms.CreateCategorie(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # save categorie to DB # DEBUG: # TODO:
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, "Le catégorie a été modifiée avec succès !")
            return redirect('categorie:indexCategorie')
    else:
        form = forms.CreateCategorie(instance=post)
        
    return render(request, 'categorie/categorie_create.html', {'form': form, 'classe_active': classe_active})


def categorie_delete(request, categorie_id):

    categorie= Categorie.objects.filter(pk=categorie_id)
    categorie.delete()
    messages.success(request, "Le catégorie a été supprimée avec succès !")
    categories = Categorie.objects.all()

    return redirect('categorie:indexCategorie')