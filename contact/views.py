from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError, send_mail
from django.http import Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
import datetime





# Contact form view

def contact(request):
    classe_active=5
    Contact_Form = ContactForm
    if request.method == 'POST':
        form = Contact_Form(request.POST)

        if form.is_valid():
            contact_name = request.POST.get('Nom')
            contact_email = request.POST.get('Email')
            contact_subject = request.POST.get('Sujet')
            contact_content = request.POST.get('Message')
            contact = form.save(commit=False)
            contact.save()
            # TO DO Fix mail send

            send_mail(
                contact_subject,
                contact_content,
                contact_email,
                ['nsitsenegaltest@gmail.com'],
                fail_silently=False,
            )

            

            # msg = EmailMessage(contact_subject,
            #                    'Here is the message.', to=[contact_email])
            # msg.send()


            return render(request, 'home.html', {'form':Contact_Form })

            #return redirect('blog:success')
    return render(request, 'contact/contact.html', locals())

def contact_detail(request, contact_id):
    classe_active = 12
    try:
        contact = Contact.objects.get(pk=contact_id)
        contact.is_read = True
        contact.save()
    except Contact.DoesNotExist:
        raise Http404("La contact n'existe pas")
    return render(request, 'contact/contact_detail.html', locals())


def contact_list(request, page=1):
    contacts = Contact.objects.order_by('-id').all()
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if request.GET.get('tag') and request.GET.get('tag') != '':
            tag = request.GET.get('tag')
            contacts = Contact.objects.filter(Q(Sujet__icontains=request.GET.get('tag')) | Q(Message__icontains=request.GET.get('tag')) | Q(Prenom__icontains=request.GET.get('tag')) | Q(Nom__icontains=request.GET.get('tag')) | Q(Email__icontains=request.GET.get('tag')))
        if request.GET.get('is_read'):
            contacts = Contact.objects.filter(is_read=True)
        if request.GET.get('is_treat'):
            contacts = Contact.objects.filter(is_treat=True)

        if request.GET.get('is_finish'):
            contacts = Contact.objects.filter(is_finish=True)

        if request.GET.get('creat_at'):
            entry_date = request.GET.get('creat_at').split('-')
            year = int(entry_date[0])
            month = int(entry_date[1])
            day = int(entry_date[2])
            contacts = Contact.objects.filter(Q(Date_modification__gte=datetime.datetime(year, month, day)))
    else:
        form = SearchForm()
    paginator = Paginator(contacts, 6)
    page_number = request.GET.get('page')
    try:
        contacts = paginator.get_page(request.GET.get('page'))
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "contact/contact_list.html", locals())

def contact_delete(request, contact_id):

    contact= Contact.objects.filter(pk=contact_id)
    contact.delete()
    messages.success(request, "La contact a été supprimée avec succès !")
    contacts = Contact.objects.all()

    return redirect('contact:indexContact')

def contact_treat(request, contact_id):
    try:
        contact = Contact.objects.get(pk=contact_id)
        contact.is_treat = True
        contact.save()
    except Contact.DoesNotExist:
        raise Http404("La contact n'existe pas")
    return redirect(f'/contact/{contact_id}')

def contact_finish(request, contact_id):
    try:
        contact = Contact.objects.get(pk=contact_id)
        contact.is_finish = True
        contact.save()
    except Contact.DoesNotExist:
        raise Http404("La contact n'existe pas")
    return redirect(f'/contact/{contact_id}')