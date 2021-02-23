from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from categorie.models import Categorie
from . import models
from .enum import *
from .models import Produit, Photos


class CreateProduit(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Libellé du produit'}), required=False)
    categorie = forms.ModelChoiceField(label='Catégorie', queryset=Categorie.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Genre'}))
    gender = forms.ChoiceField(label='Genre', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Genre'}), choices=GENDER_CHOICES)
    color = forms.ChoiceField(label='Couleur', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Couleur'}), choices = COLOR_CHOICES)
    price = forms.CharField(label="Prix", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prix d achat'}), required=False)
    purchase_price = forms.CharField(label="Prix de vente", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prix de vente'}), required=False)
    provider = forms.CharField(label="Fournisseur", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fournisseur'}), required=False)
    size_cloth = forms.ChoiceField(label='Taille', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Taille'}),choices = CLOTH_SIZE_CHOICES)
    size_shoes = forms.ChoiceField(label='Pointure', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pointure'}),choices = SHOES_SIZE_CHOICES)
    stock = forms.CharField(label="Stock", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantité'}), required=False)
    label = forms.ChoiceField(label='Label', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Label'}),choices = LABEL_CHOICES)
    marque = forms.CharField(label="Marque", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marque du produit'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"rows":5, "cols":20, 'class': 'form-control', 'placeholder': 'Caractéristiques du produit'}))

    class Meta:
        model = Produit
        fields = ['title','categorie', 'gender', 'color', 'price', 'purchase_price', 'provider', 'size_cloth', 'size_shoes', 'stock', 'label', 'marque', 'description']

class CreatePhoto(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ['photo']


# Form de Order
class CreateOrder(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['user', 'ref_code']




class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=True)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_town = forms.CharField(label="Test", widget=forms.Select(attrs={'class': 'form-control'}, choices=TOWN), required=True)

    shipping_tel = forms.CharField(required=True)
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(Pays)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))



class CreateAdresse(forms.ModelForm):
    street_address = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Libellé du produit'}), required=False)
    apartment_address = forms.CharField(label="Prix", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prix d achat'}), required=False)
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    zip = forms.CharField(label="Zip", widget=forms.Select(attrs={'class': 'form-control'}, choices=TOWN), required=True)
    address_type = forms.CharField(label="Type", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prix d achat'}), required=False)
    town = forms.CharField(label="Ville", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prix d achat'}), required=False)
    tel = forms.CharField(label="Téléphone", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prix d achat'}), required=False)
    class Meta:
        model = models.Address
        fields = ['street_address', 'apartment_address', 'country', 'zip', 'address_type', 'town', 'tel']
