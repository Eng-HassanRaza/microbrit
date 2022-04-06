# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class GetAQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    request_for_quote = models.TextField(null=True, blank=True)
    upload_design = models.FileField(upload_to='designs/')
    health_safety = models.FileField(upload_to='health_safety/',null=True,blank=True)
    quantity = models.CharField(max_length=255,null=True,blank=True)
    material_type = models.CharField(max_length=255,null=True,blank=True)
    material = models.CharField(max_length=255,null=True,blank=True)
    delivery_date = models.CharField(max_length=255,null=True,blank=True)
    custom_info = models.CharField(max_length=255,null=True,blank=True)
    company_details = models.CharField(max_length=255,null=True,blank=True)
    personal_details = models.CharField(max_length=255,null=True,blank=True)
    email = models.CharField(max_length=255,null=True,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(max_length=65, blank=True, null=True)


class ExtraInfo(models.Model):
    email = models.ForeignKey(GetAQuote, on_delete=models.CASCADE, null=True, blank=True)
    request_for_quote = models.TextField(null=True, blank=True)

