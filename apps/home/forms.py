# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import GetAQuote,ExtraInfo


# create a ModelForm
class ExtraInfoForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = ExtraInfo
        fields = "__all__"