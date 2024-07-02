from django.shortcuts import render
from .models import CustomAppModel

def listDMPView(request):
    data = CustomAppModel.objects.all()
    context = {"customdata": data}
    return render(request, "home/customlist.html", context)

# Create your views here.
