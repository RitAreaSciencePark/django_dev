from django import forms
# This import point to the external app schema!
from PRP_CDM_app.forms import FormsDefinition

class LabSwitchForm(forms.Form):
    user_labs = []
    
    def _defineChoices(self):
        choices = []
        for user_lab in self.user_labs:
            choices.append((user_lab.name,user_lab.name))
        return choices

    def __init__(self, user_labs, *args, **kwargs):
        super(LabSwitchForm,self).__init__(*args, **kwargs)
        if user_labs is not None:
            self.user_labs = user_labs
            self.fields['lab_selected'] = forms.ChoiceField(choices=self._defineChoices())

# TODO: dynamic this
def form_orchestrator(user_lab, request):
    # lablist = [labform for labform in dir(FORMS()) if not labform.startswith("__")]
    if user_lab is None:
        return None # TODO manage this
    else:
        formClass = getattr(FormsDefinition,user_lab.title() + "Form")
        return [form_factory(form_model, request=request) for form_model in formClass.content]
 

def form_factory(form_model, request):
    class CustomForm(forms.ModelForm):
        # see https://docs.djangoproject.com/en/1.9/topics/forms/ for more complex example.
        # We are using a ModelForm, it is not mandatory

        class Meta:
            model = form_model
            # fields = ['datavarchar', 'dataint']
            exclude = ['uuid','datausername']

    return CustomForm(request)

