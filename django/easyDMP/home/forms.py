from django import forms
# This import point to the external app schema!
from PRP_CDM_app.forms import FormsDefinition
from PRP_CDM_app.models import labDMP
from PRP_CDM_app.models import Users, Proposals
from PRP_CDM_app.fields import BooleanIfWhat, MultiChoicheAndOtherWidget

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
def form_orchestrator(user_lab, request, filerequest):
    # lablist = [labform for labform in dir(FORMS()) if not labform.startswith("__")]
    if user_lab is None:
        return None # TODO manage this
    else:
        # this block checks the class names into FormsDefinition to create the forms
        formClass = getattr(FormsDefinition,user_lab.title() + "Form")
        if hasattr(formClass, "exclude") and formClass.exclude is not None:
            for formdef, values in formClass.exclude.items():
                pass

        form_list = []
        # this block checks if there are some special field names to override the widgets
        widgets_list = {}
        for form_model in formClass.content:
            debug = form_model.__name__
            if hasattr(formClass, "exclude") and formClass.exclude is not None:
                exclude = formClass.exclude[form_model.__name__]
            if hasattr(form_model, "widgets") and form_model.widgets is not None:
                widgets_list = form_model.widgets
            form_list.append(form_factory(form_model, widgets_list, request=request, filerequest=filerequest, exclude_list=exclude))
        return form_list
 

def form_factory(form_model, widgets_list, request, filerequest, exclude_list):
    class CustomForm(forms.ModelForm):

        # see https://docs.djangoproject.com/en/1.9/topics/forms/ for more complex example.
        # We are using a ModelForm, it is not mandatory
        
        class Meta:
            model = form_model
            # fields = ['datavarchar', 'dataint']
            debug = widgets_list
            widgets = widgets_list
            exclude = exclude_list

        def __init__(self, *args, **kwargs):
            super(CustomForm, self).__init__(*args, **kwargs)

    return CustomForm(request,filerequest)

class DMPform(forms.ModelForm):

        # see https://docs.djangoproject.com/en/1.9/topics/forms/ for more complex example.
        # We are using a ModelForm, it is not mandatory
        
        class Meta:
            model = labDMP
            # fields = ['datavarchar', 'dataint']
            widgets = {'instrument_metadata_collection': BooleanIfWhat(yes_or_no=True),
                       'additional_enotebook_open_collection': BooleanIfWhat(yes_or_no=True),
                       'sample_standard': BooleanIfWhat(yes_or_no=True),
                       'metadata_schema_defined': BooleanIfWhat(yes_or_no=True),
                       'open_data_licence':BooleanIfWhat(yes_or_no=True),
                       }
            exclude = ['labname', 'user_id'] 


class UserDataForm(forms.ModelForm):
    class Meta:
            model = Users
            # fields = ['datavarchar', 'dataint']
            '''widgets = {'gender': forms.SelectMultiple(),
                       'legal_status': forms.SelectMultiple(),
                       'research_role': forms.SelectMultiple(),
                       }'''
            exclude = ['user_id']


class ProposalSubmissionForm(forms.ModelForm):
    class Meta:
            model = Proposals
            # fields = ['datavarchar', 'dataint']
            exclude = ['proposal_id',
                       'user_id',
                       'proposal_status',
                       'proposal_feasibility',
                       #'proposal_submission_date'
                       ]