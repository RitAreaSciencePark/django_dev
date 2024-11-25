from django.db import models
from django import forms

# Not used for now
class SelectWithOther(forms.widgets.Select):
    template_name = "select.html"

# Not used for now
class JSText(forms.TextInput):
    template_name = "jstext.html"

class MultiChoicheAndOtherWidget(forms.MultiWidget):
    template_name = "jsmultipleandother.html"   # TODO: check if this is vulnerable to injection (I think not), easydmp/widgets/...

    def __init__(self, choices):
        choices = choices+[('other','other'),]
        widgets = [
            forms.Select(choices=choices),
            forms.TextInput(attrs={'placeholder':'Other'}),
        ]
        super(MultiChoicheAndOtherWidget, self).__init__(widgets)

    def decompress(self, value):
        if not value:
            return [None, None]
        return value

    def value_from_datadict(self, data, files, name):
        value1, value2 = super().value_from_datadict(data, files, name)
        if(value1 == 'Other'):
            return 'Other: {}'.format(value2)
        else:
            return value1
    
    def subwidgets(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        return context['widget']['subwidgets']
    
class BooleanIfWhat(forms.MultiWidget):
    template_name = "jsbooleanifwhat.html"   # TODO: check if this is vulnerable to injection (I think not), easydmp/widgets/...
    yes_or_no = False

    def __init__(self, yes_or_no):
        widgets = [
            forms.CheckboxInput(),
            forms.TextInput(attrs={'placeholder':'...'}),
        ]
        self.yes_or_no = yes_or_no
        super(BooleanIfWhat, self).__init__(widgets)

    def decompress(self, value):
        if not value:
            return [None, None]
        if value[:3] == 'Yes':
            return [True,value[5:]]
        else:
            return [False,value[5:]]

    def value_from_datadict(self, data, files, name):
        value1, value2 = super().value_from_datadict(data, files, name)
        if(value1 == self.yes_or_no):
            if(self.yes_or_no):
                return 'Yes: {}'.format(value2)
            else:
                return 'No: {}'.format(value2)
        else:
            if(self.yes_or_no):
                return 'No'
            else:
                return 'Yes'
    
    def subwidgets(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        return context['widget']['subwidgets']
    
    def get_context(self, name, value, attrs):
        attrs['yes_or_no'] = self.yes_or_no
        context = super().get_context(name, value, attrs)
        return context