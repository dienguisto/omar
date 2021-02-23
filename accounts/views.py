from typing import re

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, ProfilEditForm, \
    AccountEditForm

#from django.core.mail import send_mail
from accounts.models import Profil, Account
from categorie.models import Categorie
from product.models import Order


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user =  form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password1'))
            new_user.save()
            Profil.objects.create(account=new_user)
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return HttpResponseRedirect(reverse("home"))
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    """
    send_mail(
        'That your subject',
        'That your message body',
        'from@yourdjangoapp.com',
        ['mbayediawthiam@gmail.com'],
        fail_silently=False,
    )
    """   
    context = {}

    user = request.user
    if user.is_authenticated: 
        return HttpResponseRedirect(reverse("home"))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return HttpResponseRedirect(reverse("home"))

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "accounts/login.html", context)


def account_view(request):

    if not request.user.is_authenticated:
            return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(

            initial={
                    "email": request.user.email, 
                    "username": request.user.username,
                }
            )

    context['account_form'] = form

    # blog_posts = BlogPost.objects.filter(author=request.user)
    # context['blog_posts'] = blog_posts

    return render(request, "accounts/account_old.html", context)


def must_authenticate_view(request):
    return render(request, 'accounts/must_authenticate.html', {})



def profile_view(request):
    categories = Categorie.objects.all()
    orders = Order.objects.filter(user=request.user)
    if request.method == 'POST':
        user_form = AccountEditForm(data=request.POST or None, instance= request.user)
        profil_form = ProfilEditForm(data=request.POST or None, instance= request.user.profil, files=request.FILES)
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        telephone = request.POST["telephone"]
        addressseller = request.POST["addressseller"]


        user=Account.objects.get(id=request.user.id)
        profil = Profil.objects.get(account=user)
        if request.FILES:
            profil.image = request.FILES['image']
        profil.save()
        user.firstname=firstname
        user.lastname=lastname
        user.username=username
        user.telephone=telephone
        user.addressseller=addressseller
        user.save()
        return redirect("accounts:profile")

    else:
        user_form = AccountEditForm(instance= request.user)
        profil_form = ProfilEditForm(instance= request.user)

    context={
        "user_form": user_form,
        "profil_form": profil_form,
        "categories": categories,
        "orders": orders,
    }
    return render(request, 'accounts/profile.html', context)