from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact #or whatever object
        fields = ['Nom', 'Prenom', 'Email', 'Message']

class SearchForm(forms.Form):
    tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'tag-input', 'placeholder':'Chercher un message'}), required=False, label='')
    is_read = forms.BooleanField(required=False, label='Lu')
    is_treat = forms.BooleanField(required=False, label='Traité')
    is_finish = forms.BooleanField(required=False, label='Terminé')
    creat_at = forms.DateTimeField(required=False, label="Date", widget=forms.TextInput(attrs={'placeholder':'Format: AAAA-MM-DD'}))