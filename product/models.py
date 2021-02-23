from django.db import models
from categorie.models import Categorie
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django_countries.fields import CountryField
from .enum import *
from django.utils import timezone
from django.contrib import messages


# Create your models here.
from omar import settings


class Produit(models.Model):
    title = models.CharField("Nom du produit", max_length=250)
    code_ref = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField('Prix')
    purchase_price = models.FloatField("Prix d'achat", blank=True, null=True)
    sale_price = models.FloatField(blank=True, null=True)
    discount_price = models.FloatField("Prix réduit", blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='produits')
    label = models.CharField("Label", choices=LABEL_CHOICES, max_length=1)
    description = models.TextField("Description")
    gender = models.CharField("Genre", choices=GENDER_CHOICES, max_length=1, default='X')
    color = models.CharField("Couleur",choices=COLOR_CHOICES, max_length=2, default='X')
    size_cloth = models.CharField("Taille", choices=CLOTH_SIZE_CHOICES, max_length=2, default='X')
    size_shoes = models.CharField("Pointure", choices=SHOES_SIZE_CHOICES, max_length=2, default='X')
    star = models.IntegerField(default=0)
    provider = models.CharField("Fournisseur", max_length=100, default='proximarket')
    stock = models.IntegerField(default=1)
    status = models.CharField("Statut", choices=STATUS_CHOICES, max_length=1, default='D')
    origin = models.CharField(choices=ORIGIN, max_length=2, default='X')
    marque = models.CharField(max_length=100, blank=True, null=True, default='Générique')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)


    def __str__(self):
        return self.title

# Create your models here.
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product:detailProduit', args=[self.pk])

    def get_absolute_url(self):
        return reverse("product:product", kwargs={
            'pk': self.pk
        })


    def get_add_to_cart_url(self):
        return reverse("product:add-to-cart", kwargs={
            'pk': self.pk
        })

    def get_add_to_cart_quick_url(self):
        return reverse("product:add-to-cart-quick", kwargs={
            'pk': self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("product:remove-from-cart", kwargs={
            'pk': self.pk
        })






class Photos(models.Model):
    photo = models.ImageField(blank=True, null=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, related_name='photos')

    def __str__(self):
        return self.id

class OrderProduit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE, default=None)
    ordered = models.BooleanField(default=False)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    sessionID = models.CharField(max_length=200, default='X')

    def __str__(self):
        return f"{self.quantity} of {self.produit.title}"

    def get_total_produit_price(self):
        return self.quantity * self.produit.price

    def get_total_discount_produit_price(self):
        return self.quantity * self.produit.discount_price

    def get_amount_saved(self):
        return self.get_total_produit_price() - self.get_total_discount_produit_price()

    def get_final_price(self):
        if self.produit.discount_price:
            return self.get_total_discount_produit_price()
        return self.get_total_produit_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    produits = models.ManyToManyField(OrderProduit)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    payment_option = models.CharField(max_length=2, blank=True, null=True)
    sessionID = models.CharField(max_length=200, default='X', null=True)

    '''
    1. Produit added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.sessionID

    def get_total(self):
        total = 0
        for order_produit in self.produits.all():
            total += order_produit.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


    def get_produits(self):
        print(self.produits.all())
        return self.produits.all()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    town  = models.CharField(max_length=10, choices=TOWN, default="1")
    telephone = models.CharField(max_length=15, default="X")

    def __str__(self):
        return self.user.username



class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"



