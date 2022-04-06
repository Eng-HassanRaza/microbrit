# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import stripe
from django.views.generic import View
stripe.api_key = settings.STRIPE_SECRET_KEY

# This is your test secret API key.


from .models import GetAQuote
from .forms import ExtraInfoForm

from ..frontend.forms import GetAQuoteForm


def send_email(email,extra_info):
    subject = 'Please provide extra info'
    message =  extra_info
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )
    return True

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    if request.user.is_staff:
        quotes = GetAQuote.objects.all()
        context['quotes'] = quotes
        html_template = loader.get_template('staff/index.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect('/dashboard/customer/')

@login_required(login_url="/login/")
def customer(request):
    context = {'segment': 'index'}
    quotes = GetAQuote.objects.filter(user=request.user)
    context['quotes'] = quotes
    html_template = loader.get_template('customer/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def customer_qoute_detail(request,id):
    context = {'segment': 'index'}
    quote = GetAQuote.objects.filter(id=id).first()
    context['quote'] = quote
    context['quote25percent']=quote.price/4
    context['quote50percent']=quote.price/2
    context['quote75percent']=(quote.price/4)*3
    # if request.method == 'POST':
    #     pay_amount = request.POST['payamount']
    #     print(pay_amount)
    html_template = loader.get_template('customer/extra-info.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def create_checkout_session(request):
    host = request.get_host()
    price1 = request.POST['payamount']
    price = int(float(price1))
    username = request.user.username
    checkout_session = stripe.checkout.Session.create(

        line_items=[
            {
                'price_data': {
                    'currency':'USD',
                    'unit_amount':price*100,
                    'product_data':{
                        'name': username
                    },
                },
                'quantity':1,
            },
        ],
        mode='payment',
        success_url= "http://{}{}".format(host,reverse('home:payment-success')),
        cancel_url= "http://{}{}".format(host,reverse('home:payment-cancel')),
    )
    return redirect(checkout_session.url, code=303)

@login_required(login_url="/login/")
def paymentSuccess(request):

    context = {
        'payment_status':'Payment Successfully Proccessed'
    }
    html_template = loader.get_template('customer/success.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def paymentCancel(request):

    context = {
        'payment_status': 'cancel'
    }
    html_template = loader.get_template('customer/cancel.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def detail_quote(request,id):
    context = {'segment': 'detail-quote'}
    quote = GetAQuote.objects.filter(id=id).first()
    context['quote'] = quote
    html_template = loader.get_template('staff/detail-quote.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def delete_quote(request,id):
    context = {'segment': 'detail-quote'}
    quote = GetAQuote.objects.filter(id=id).delete()
    return redirect("/dashboard/")

@login_required(login_url="/login/")
def extra_info(request,id):
    context = {'segment': 'detail-quote'}
    quote = GetAQuote.objects.filter(id=id).first()
    context['quote'] = quote
    form = ExtraInfoForm()
    if request.method == "POST":
        user_exist = User.objects.filter(email=request.POST['email'])
        dashboard_url = request.build_absolute_uri('/dashboard/')
        if not user_exist:
            user_obj = User(username=request.POST['email'],email=request.POST['email'])
            user_obj.save()
            my_password = User.objects.make_random_password()
            user_obj.set_password(my_password)
            user_obj.save()
            getaqoute = GetAQuote.objects.filter(email=request.POST['email']).update(user=user_obj)
            quotedprice = request.POST['price']
            GetAQuote.objects.filter(email=request.POST['email']).update(price=quotedprice)
            extra_info = f'Please login using below details and provide below info \r Email: {user_obj.email} \r Password: {my_password} \r' + request.POST['request_for_quote']+f'\r\r Dashboard Link: {dashboard_url} \r\r Total Price: {quotedprice}'
        else:
            getaqoute = GetAQuote.objects.filter(email=request.POST['email']).update(user=request.user)
            quotedprice = request.POST['price']
            GetAQuote.objects.filter(email=request.POST['email']).update(price=quotedprice)
            extra_info = f'Please login to your account and provide below info \r' + \
                         request.POST['request_for_quote'] + f'\r\r Dashboard Link: {dashboard_url} \r\r Total Price: {quotedprice}'

        send_email(request.POST['email'],extra_info)

        redirect('/dashboard/')
    context['form'] = form
    html_template = loader.get_template('staff/ask-extra-info-email.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def create_quote_staff(request):
    context = {'segment': 'index'}
    form = GetAQuoteForm()
    if request.method == 'POST':
        form = GetAQuoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context['form'] = form
    html_template = loader.get_template('staff/create-quote-staff.html')
    return HttpResponse(html_template.render(context, request))
