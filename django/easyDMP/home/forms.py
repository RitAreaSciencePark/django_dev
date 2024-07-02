from django import forms
# This import point to the external app schema!
from PRP_CDM_app.models import CustomAppModel


class CustomForm(forms.ModelForm):
    
    # see https://docs.djangoproject.com/en/1.9/topics/forms/ for more complex example.
    # We are using a ModelForm, it is not mandatory
    class Meta:
        model = CustomAppModel
        fields = ['datavarchar', 'dataint']