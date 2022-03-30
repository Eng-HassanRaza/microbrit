# import form class from django
from django import forms

# import GeeksModel from models.py
from ..home.models import GetAQuote


# create a ModelForm
class GetAQuoteForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = GetAQuote
        fields = "__all__"