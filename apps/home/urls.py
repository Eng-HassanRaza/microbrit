# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
app_name="home"
urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('detail-quote/<int:id>', views.detail_quote, name='detail-quote'),
    path('delete-quote/<int:id>', views.delete_quote, name='delete-quote'),
    path('extra-info/<int:id>', views.extra_info, name='extra-info'),
    path('customer/', views.customer, name='customer'),
    path('customer-provide-extra-info/<int:id>', views.customer_qoute_detail, name='customer_qoute_detail'),
    path('create-quote-staff', views.create_quote_staff, name='create_quote_staff'),

    #Stripe Payment
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.paymentSuccess, name='payment-success'),
    path('cancelled/', views.paymentCancel, name='payment-cancel'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
