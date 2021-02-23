from django.db import models


# Create your models here.

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    update = models.DateTimeField(auto_now_add=True)
    is_sale  = models.BooleanField(default=True)
    is_actif  = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

    def get_produits(self):
        return self.produits.all()