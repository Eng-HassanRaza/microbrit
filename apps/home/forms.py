# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import GetAQuote,ExtraInfo


# create a ModelForm
class GetAQuoteForm(forms.ModelForm):
    class Meta:
        model = GetAQuote
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(GetAQuoteForm, self).__init__(*args, **kwargs)

        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control'

class ExtraInfoForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = ExtraInfo
        fields = "__all__"
