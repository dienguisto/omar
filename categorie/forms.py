from django import forms
from . import models

class CreateCategorie(forms.ModelForm):
    class Meta:
        model = models.Categorie
        fields = ['nom']
