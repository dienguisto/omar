from categorie.models import Categorie
from product.models import Produit, Order
from django.shortcuts import render, redirect
from django.views.generic import ListView


class HomeView(ListView):
    # model = Item
    # paginate_by = 10
    # version = "1.0.0"
    # context_object_name = 'product_list'
    # template_name = "home.html"
    def get(self, *args, **kwargs):
        classe_active = 'accueil'
        object_list_last = Produit.objects.all().order_by('-id')[:4]
        categories = Categorie.objects.all()
        object_better_seller = Order.objects.all()

        """
        object_list_woman = grouped(Produit.objects.filter(gender='F'), 8)
        object_list_man = grouped(Produit.objects.filter(gender='H'), 8)
        object_list_kid = grouped(Produit.objects.filter(gender='E'), 8)
        object_list_other = grouped(Produit.objects.filter(gender='X'), 8)
        object_list_tech = grouped(Produit.objects.filter(categorie=1), 8)
        """

        object_list_woman = Produit.objects.filter(gender='F')
        object_list_man = Produit.objects.filter(gender='H')
        object_list_kid = Produit.objects.filter(gender='E')
        object_list_other = Produit.objects.filter(gender='X')
        object_list_tech = Produit.objects.filter(categorie__nom='Informatique')


        #TODO la valeur de catégorie est a changer
        object_list_woman = list(object_list_woman)
        object_list_man = list(object_list_man)
        object_list_kid = list(object_list_kid)
        object_list_other = list(object_list_other)
        # object_list_tech = list(object_list_tech)

        context = {
            'object_list_woman': object_list_woman,
            'object_list_man': object_list_man,
            'object_list_kid': object_list_kid,
            'object_list_other': object_list_other,
            'object_list_tech': object_list_tech,
            'object_list_last': object_list_last,
            'object_better_seller': object_better_seller,
            'classe_active': classe_active,
            'categories': categories,
        }

        print('-------------------------------------------------------------------------------------')
        response = render(self.request, 'home.html', context)
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')   # TODO à optimiser pour tenir compte des users qui utlisent des VPNs ou IPs variables
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            print(ip)
            response.set_cookie('sessionID', ip)
        else:
            ip = self.request.META.get('REMOTE_ADDR')
            print(ip)
            response.set_cookie('sessionID', ip)

            """
        if not self.request.session.session_key:
            self.request.session.create()
        sessionID = self.request.session.session_key
        print(sessionID)
        response = render(self.request, 'home.html', context)
        response.set_cookie('sessionID', sessionID, max_age=9999999999)"""
        print('-------------------------------------------------------------------------------------')

        return response

