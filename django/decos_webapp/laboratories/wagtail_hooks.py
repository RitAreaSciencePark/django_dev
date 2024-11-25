from django.urls import path

from .views import AddLabView
from wagtail import hooks

@hooks.register('register_admin_urls')
def register_calendar_url():
    return [
        path('add-laboratory/', AddLabView, name='add-laboratory'),
    ]