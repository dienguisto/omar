from django.contrib import admin
from .models import Produit

class ProduitPhotoInline(admin.TabularInline):
    model = Produit
    extra = 3

class ProduitAdmin(admin.ModelAdmin):
    inlines = [ ProduitPhotoInline, ]

# Register your models here.
admin.site.register(Produit)



