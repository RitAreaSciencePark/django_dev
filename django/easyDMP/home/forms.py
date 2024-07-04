from django import forms
# This import point to the external app schema!
from PRP_CDM_app.models import CustomAppModel

class LabSwitchForm(forms.Form):
    user_labs = []
    picked = []

    def _defineChoices(self):
        choices = []
        for user_lab in self.user_labs:
            choices.append((user_lab.name,user_lab.name))
        return choices

    def __init__(self, user_labs, *args, **kwargs):
        super(LabSwitchForm,self).__init__(*args, **kwargs)
        self.user_labs = user_labs
        self.fields['picked'] = forms.MultipleChoiceField(choices=self._defineChoices(), widget=forms.CheckboxSelectMultiple)


def form_orchestrator(user_lab, request):
    if user_lab is None:
        return form_factory(CustomAppModel, request=request)
    else:
        return form_factory(CustomAppModel, request=request)
    
def form_factory(form_model, request):
    class CustomForm(forms.ModelForm):

        # see https://docs.djangoproject.com/en/1.9/topics/forms/ for more complex example.
        # We are using a ModelForm, it is not mandatory
        class Meta:
            model = form_model
            # fields = ['datavarchar', 'dataint']
            exclude = ['datausername']
    return CustomForm(request)
