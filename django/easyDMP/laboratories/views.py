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
