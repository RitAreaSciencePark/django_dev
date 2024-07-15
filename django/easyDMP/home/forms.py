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
        # this block checks the class names into FormsDefinition to create the forms
        formClass = getattr(FormsDefinition,user_lab.title() + "Form")
        form_list = []
        # this block checks if there are some special field names to override the widgets
        widgets_list = {}
        for form_model in formClass.content:
            if hasattr(form_model, "widgets") and form_model.widgets is not None:
                widgets_list = form_model.widgets
            form_list.append(form_factory(form_model, widgets_list, request=request))
        return form_list
 

def form_factory(form_model, widgets_list, request):
    class CustomForm(forms.ModelForm):

        # see https://docs.djangoproject.com/en/1.9/topics/forms/ for more complex example.
        # We are using a ModelForm, it is not mandatory
        
        class Meta:
            model = form_model
            # fields = ['datavarchar', 'dataint']
            debug = widgets_list
            widgets = widgets_list
            exclude = ['uuid','datausername']

        def __init__(self, *args, **kwargs):
            super(CustomForm, self).__init__(*args, **kwargs)
    return CustomForm(request)

