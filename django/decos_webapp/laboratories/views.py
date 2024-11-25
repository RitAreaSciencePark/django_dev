from django.shortcuts import render

# Create your views here.
import calendar

from django.http import HttpResponse
from django.utils import timezone
from .forms import AddNewLabForm
from django.contrib.auth.models import Group
from django.db.models import Model


def AddLabView(request):

    if request.method == 'POST':
        form = AddNewLabForm(data=request.POST)
        if form.is_valid():
            lab_id = form.cleaned_data["lab_id"]
            try:
                lab = Group.objects.get(name=lab_id)
            except Group.DoesNotExist as e:
                lab = Group(name=form.cleaned_data["lab_id"],laboratory= True)
                lab.save()
            form.save()
        else:
            errors = form.errors
            pass
    
    form = AddNewLabForm()

    return render(request, 'laboratory_form.html', {'form' : form})

## -----

from django import forms

from wagtail.users.forms import GroupForm as WagtailGroupForm

from PRP_CDM_app.models import Laboratories


class GroupForm(WagtailGroupForm):
    laboratories = forms.CharField()

    class Meta(WagtailGroupForm.Meta):
        fields = WagtailGroupForm.Meta.fields + ("laboratories",)

    def __init__(self, initial=None, instance=None, **kwargs):
        if instance is not None:
            if initial is None:
                initial = {}
            initial["laboratories"] = instance.adgroups.all()
        super().__init__(initial=initial, instance=instance, **kwargs)

    def save(self, commit=True):
        instance = super().save()
        instance.laboratories.set(self.cleaned_data["laboratories"])
        return instance
    
from wagtail.users.views.groups import GroupViewSet as WagtailGroupViewSet

from .forms import AddNewLabForm
    
class GroupViewSet(WagtailGroupViewSet):
    def get_form_class(self, for_update=False):
        return AddNewLabForm