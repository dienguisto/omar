from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import RegistrationSellerForm
from categorie.models import Categorie
from .forms import CreateProduit, CreateOrder, CheckoutForm, CouponForm
from .models import Produit, Photos, Order, Produit, OrderProduit, Address, Coupon
from . import forms
from django.contrib import messages
from django.forms import formset_factory, modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from django.utils import timezone
import random
import string

from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string

# Create your views here.

def product_list(request):
    classe_active = 'produit'
    produits = Produit.objects.all()

    return render(request, "product/product_list.html", locals())


def product_create(request):
    classe_active = 'produit'
    Photoformset = modelformset_factory(Photos, fields=('photo',), extra=4)
    if request.method == 'POST':
        print('test1')
        form = CreateProduit(request.POST or None)
        formset = Photoformset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            print('test2')
            produit = form.save(commit=False)
            produit.code_ref = create_ref_code()
            produit.agent = request.user
            produit.save()
            messages.success(request, "Le produit a été crée avec succès !")
            for f in formset:
                try:
                    photo = Photos(produit=produit, photo=f.cleaned_data['photo'])
                    photo.save()
                except Exception as e:
                    print(e)
                    break
            return redirect('product:indexProduit')




    else:
        form = CreateProduit()
        formset = Photoformset(queryset=Photos.objects.none())
    context = {
        'form': form,
        'formset': formset,
        'classe_active': classe_active,
    }

    return render(request, 'product/product_create.html', context)


def product_detail(request, product_id):
    classe_active = 'produit'
    try:
        # produits = Produit.objects.all()
        produit = Produit.objects.get(pk=product_id)
        # photos = Photos.objects.exclude(photo__isnull=True).exclude(photo__exact='').filter(produit=product_id)
        lesphotos = produit.photos.all()
    except Produit.DoesNotExist:
        raise Http404("Le produit n'existe pas")
    return render(request, 'product/product_detail.html', locals())


def view_product(request, product_id):
    categories = Categorie.objects.all()
    try:
        produit = Produit.objects.get(pk=product_id)
        photos = produit.photos.all()
        classe_active = produit.categorie.nom
    except Produit.DoesNotExist:
        raise Http404("Le produit n'existe pas")
    return render(request, 'product/view_product.html', locals())


def product_edit(request, id):
    classe_active = 'produit'
    produit = get_object_or_404(Produit,id=id)
    Photoformset = modelformset_factory(Photos, fields=('photo',), extra=4, max_num=4)
    classe_active = 3
    if request.method == 'POST':
        form = CreateProduit(request.POST or None, instance=produit)
        formset = Photoformset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            form.save()
            messages.success(request, "Le produit a été crée avec succès !")
            data = Photos.objects.filter(produit=produit)

            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo = Photos(produit=produit, photo=f.cleaned_data.get('photo'))
                        photo.save()
                    elif f.cleaned_data['photo'] is False:
                        photo=Photos.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete()
                    else:
                        photo = Photos(produit=produit, photo=f.cleaned_data.get('photo'))
                        d = Photos.objects.get(id=data[index].id)
                        d.photo = photo.photo
                        d.save()



            return redirect('product:indexProduit')


    else:
        form = CreateProduit(instance=produit)
        formset = Photoformset(queryset=Photos.objects.filter(produit=produit))
    context = {
        'form': form,
        'produit': produit,
        'formset': formset,
    }

    return render(request, 'product/product_edit.html', context)


def product_delete(request, product_id):
    classe_active = 'produit'
    produit = Produit.objects.filter(pk=product_id)
    produit.delete()
    messages.success(request, "Le produit a été supprimé avec succès !")
    produits = Produit.objects.all()

    return redirect('product:indexProduit')


# class OrderSummaryView(LoginRequiredMixin, View):
def OrderSummaryView(request):
    try:
        categories = Categorie.objects.all()
        sessionID = request.COOKIES.get('sessionid')
        order = Order.objects.get(sessionID=sessionID, ordered=False)
        if order:
            produits = order.produits.all()
            if produits:
                cat = produits[0].produit.categorie
                classe_active = cat.nom
                interestedProduits = Produit.objects.filter(categorie=cat)[:8]

            else:
                interestedProduits = Produit.objects.all()[:8]

            best_sellers = getBestSellersProducts()
            context = {
                'object': order,
                'interestedProduits': interestedProduits,
                'best_sellers': best_sellers,
                'categories': categories,
                'classe_active': classe_active,
            }
            return render(request, 'product/order_summary.html', context)
        else:
            return redirect(request.META['HTTP_REFERER'])

    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect("/")


def getBestSellersProducts():
    # Here we get product that must selled
    orders = Order.objects.all()[:20]  # TODO Ici faudra filtrer par les mieux vendus

    # after we get related categories and set the list
    produits = []
    if orders:
        for o in orders:
            try:
                orderProduits = o.produits.all()
                print("--------------------------333--------------------------")
                print(orderProduits)
                print("--------------------------333--------------------------")
                if orderProduits:
                    cat = orderProduits[0].produit.categorie
                    tmp = Produit.objects.filter(categorie=cat)[:1]
                    produits.append(tmp)
            except:
                print('::::::::: Exception in getBestSellersProducts:::::::::')

    if len(produits) == 0:
        produits = Produit.objects.all()[:20]

    return produits

def navShopView(request, slug):

    classe_active = slug
    categories = Categorie.objects.all()
    produits = Produit.objects.filter(categorie__nom=slug)
    paginator = Paginator(produits, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': produits,
        'classe_active': classe_active,
        'page_obj': page_obj,
        'categories': categories,
    }
    print(produits)
    return render(request, 'product/shop.html', context)


class SellerView(View):
    def get(self, *args, **kwargs):
        form = RegistrationSellerForm()
        context = {
            'form': form
        }
        return render(self.request, "product/seller.html", context)




def order_list(request):
    classe_active = 'order'
    orders = Order.objects.all()
    return render(request, "order/order_list.html", locals())

def order_create(request):
    classe_active = 'order'
    orders = Order.objects.all()
    return render(request, "order/order_create.html", locals())

def order_detail(request, order_id):
    classe_active = 'order'
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404("La commande n'existe pas")
    return render(request, 'order/order_detail.html', locals())

def order_edit(request, order_id):
    classe_active = 'order'
    post = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = CreateOrder(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # save order to DB # DEBUG: # TODO:
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, "Le order a été mofifié avec succès !")
            return redirect('order:indexOrder')
    else:
        form = CreateOrder(instance=post)

    return render(request, 'order/order_create.html', {'form': form, 'classe_active': classe_active})

def order_delete(request):
    classe_active = 'order'
    orders = Order.objects.all()
    return render(request, "order/order_list.html", locals())


def add_to_cart(request, pk):
    sessionID = request.COOKIES.get('sessionid')
    produit = get_object_or_404(Produit, pk=pk)
    order_produit, created = OrderProduit.objects.get_or_create(
        produit=produit,
        sessionID=sessionID,
        ordered=False,
        user=request.user
    )
    order_qs = Order.objects.filter(sessionID=sessionID, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order produit is in the order
        if order.produits.filter(produit__pk=produit.pk).exists():
            order_produit.quantity += 1
            order_produit.save()
            messages.info(request, "Quantité mise à jour.")
            # return redirect("product:order-summary")
        else:
            order.produits.add(order_produit)
            messages.info(request, "L'article a été bien ajouté dans le panier.")
            # return redirect("product:order-summary")
    else:
        order_produit.size_cloth = request.POST.get("size_cloth")
        order_produit.size_shoes = request.POST.get("size_shoes")
        order_produit.color = request.POST.get("color")
        ordered_date = timezone.now()
        order = Order.objects.create(sessionID=sessionID, ordered_date=ordered_date, ref_code=create_ref_code_order())
        order.produits.add(order_produit)
        messages.info(request, "L'article a été bien ajouté dans le panier.")

    """
    order = Order.objects.get(user=request.user, ordered=False)
    context = {
        'object': order
    }
    return render(request, 'product/order_summary.html', context)"""
    # return redirect("product:order-summary")""""

    return redirect("product:order-summary")

def create_ref_code():
    while True:
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        if not Produit.objects.filter(code_ref=code).exists():
            return code


def create_ref_code_order():
    while True:
        print('------------------------Trying to generate code ref order-----------------------')
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if not Order.objects.filter(ref_code=code).exists():
            return code


def add_to_cart_quick(request, pk):
    print('----------------------------sessionID')
    sessionID = request.COOKIES.get('sessionid')
    print(sessionID)
    print('----------------------------sessionID')

    produit = get_object_or_404(Produit, pk=pk)
    order_produit, created = OrderProduit.objects.get_or_create(
        produit=produit,
        sessionID=sessionID,
        ordered=False,
        user=request.user
    )
    order_qs = Order.objects.filter(sessionID=sessionID, ordered=False) # TODO We use session for order and after terminated we remove juste session column in order and update order table with user informations
    if order_qs.exists():
        order = order_qs[0]
        # check if the order produit is in the order
        if order.produits.filter(produit__pk=produit.pk).exists():
            order_produit.quantity += 1
            order_produit.save()
            messages.info(request, "Quantité mise à jour.")
            # return redirect("product:order-summary")
        else:
            order.produits.add(order_produit)
            messages.info(request, "L'article a été bien ajouté dans le panier.")
            # return redirect("product:order-summary")
    else:
        order_produit.size_cloth = "X"
        order_produit.size_shoes = "X"
        order_produit.color = "X"
        ordered_date = timezone.now()
        order = Order.objects.create(sessionID=sessionID, ordered_date=ordered_date, ref_code=create_ref_code_order())
        order.produits.add(order_produit)
        messages.info(request, "L'article a été bien ajouté dans le panier.")

    return redirect("product:order-summary")


def remove_from_cart(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order produit is in the order
        if order.produits.filter(produit__pk=produit.pk).exists():
            order_produit = OrderProduit.objects.filter(
                produit=produit,
                user=request.user,
                ordered=False
            )[0]
            order.produits.remove(order_produit)
            order_produit.delete()
            messages.info(request, "This produit was removed from your cart.")
            return redirect("product:order-summary")
        else:
            messages.info(request, "This produit was not in your cart")
            return redirect("product:product", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product:product", pk=pk)

def remove_single_produit_from_cart(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    sessionID = request.COOKIES.get('sessionid')
    order = Order.objects.get(sessionID=sessionID, ordered=False)
    if order:
        # check if the order produit is in the order
        if order.produits.filter(produit__pk=produit.pk).exists():
            order_produit = OrderProduit.objects.filter(
                produit=produit,
                user=request.user,
                ordered=False
            )[0]
            if order_produit.quantity > 1:
                order_produit.quantity -= 1
                order_produit.save()
            else:
                order.produits.remove(order_produit)
            messages.info(request, "La quantité a été mise à jour.")
            return redirect("product:order-summary")
        else:
            messages.info(request, "Le produit n'est pas dans votre carte")
            return redirect("product:product", pk=pk)
    else:
        messages.info(request, "Vous n'avez pas une commande")
        return redirect("product:product", pk=pk)


def CheckoutView(request):
    categories = Categorie.objects.all()
    adresse, created  = Address.objects.update_or_create(
        user=request.user
    )
    sessionID = request.COOKIES.get('sessionid')
    order = Order.objects.get(sessionID=sessionID, ordered=False)
    if order:
        produits = order.produits.all()
        if produits:
            cat = produits[0].produit.categorie
            classe_active = cat.nom
            interestedProduits = Produit.objects.filter(categorie=cat)[:8]

        else:
            interestedProduits = Produit.objects.all()[:8]

        best_sellers = getBestSellersProducts()

    if request.method == 'POST':
        street_address = request.POST.get("street_address","")
        apartment_address = request.POST.get("apartment_address")
        country = request.POST.get("country")
        zip = request.POST.get("zip")
        address_type = request.POST.get("address_type")
        town = request.POST.get("town")
        telephone = request.POST.get("telephone")


        adresse.street_address = street_address
        adresse.apartment_address = apartment_address
        adresse.country = country
        adresse.zip = zip
        adresse.address_type = address_type
        adresse.town = town
        adresse.telephone = telephone




        order.ordered = True
        order.save()
        nom = request.user.lastname
        prenom = request.user.firstname
        email = request.user.email
        d1 = { 'nom': nom }




        subject, from_email, to = 'hello', 'eldieng10@gmail.com', email
        html_content = render_to_string('mail/email.html', d1)
        text_content = render_to_string('mail/email.txt', d1)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        adresse.save()
        messages.success(request, "Votre commande a été validée avec succes ! ")
        messages.success(request, "Vous allez recevoir un mail de confirmation")

        return redirect('home')

    else:
        form = forms.CreateAdresse()

    context = {
        'form': form,
        'adresse': adresse,
        'categories': categories,
        'order': order,
    }
    return render(request, 'product/checkout.html', context)


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("product:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("product:checkout")

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("product:checkout")

