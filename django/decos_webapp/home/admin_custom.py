from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from api.models import Project

def add_laboratory_group(lab_name):
    new_group, created = Group.objects.get_or_create(name=lab_name)