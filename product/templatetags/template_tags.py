from django import template
from product.models import Order, Address
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render
# from django.utils.translation import to_locale, get_language
# from babel.numbers import format_number

register = template.Library()


@register.filter
def cart_item_count(request):
    # if user.is_authenticated:
    try:
        qs = Order.objects.filter(sessionID=request.COOKIES.get('sessionID'), ordered=False)
        if qs.exists():
            return qs[0].items.count()
    except:
        print("Cet utilisateur n'a pas de commande.")
        
    return 0

@register.filter
def cart_total(request):
    # if user.is_authenticated:
    try:
        qs = Order.objects.filter(sessionID=request.COOKIES.get('sessionID'), ordered=False)
        if qs.exists():
            return "{} Fcfa".format(qs[0].get_total())
    except:
        print("Cet utilisateur n'a pas de commande.")
        
    return '0'

@register.filter
def cart_items(request):
    try:
        order = Order.objects.get(sessionID=request.COOKIES.get('sessionID'), ordered=False)
        return order.items.all()
    except ObjectDoesNotExist:
        print("Cet utilisateur n'a pas de commande.")

"""
@register.filter
def user_address(order):
    try:
        address = Address.objects.get(id=order.id, user__pk=order.user.id)
        return adresse
    except ObjectDoesNotExist:
        print("Cet utilisateur n'a pas renseigné d'adresse.")
"""
"""
@register.filter       
def format_currency(context, number, locale = None):
    if locale is None:
        locale = to_locale(get_language())
    return format_number(number, locale = locale)
    """
