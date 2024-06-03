
from django import forms

from home.models import CustomFormData


class CustomForm(forms.ModelForm):
    """
    A form for suggesting an ice cream flavour. Here we're using a Django ModelForm, but this could
    be as simple or as complex as you like -
    see https://docs.djangoproject.com/en/1.9/topics/forms/
    """
    class Meta:
        model = CustomFormData
        fields = ['data0', 'data1']
