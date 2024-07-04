from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)

from django.conf import settings
from django.shortcuts import render, redirect
from django.db import connections

from django.contrib.auth.models import User

from .forms import form_orchestrator, LabSwitchForm

@register_setting
class HeaderSettings(BaseGenericSetting):
    header_text = RichTextField(blank=True)
    prp_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("prp_icon"),
                FieldPanel("header_text"),
            ],
            "Header Static",
        )
    ]

@register_setting
class FooterSettings(BaseGenericSetting):

    footer_text = RichTextField(blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    github_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel("footer_text"),
        MultiFieldPanel(
            [
                FieldPanel("github_url"),
                FieldPanel("github_icon"),
            ],
            "Footer Links",
        )
    ]

class HomePage(Page):
    intro = models.CharField(max_length=250, default="")
    body = RichTextField(blank=True)
    content_panels = [
    FieldPanel("title"),
    FieldPanel("intro"),
    FieldPanel("body"),
    ]

class SampleEntryForm(Page):
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
        max_length=255, help_text="Title text to use for the 'thank you' page")

    # Note that there's nothing here for specifying the actual form fields -
    # those are still defined in forms.py. There's no benefit to making these
    # editable within the Wagtail admin, since you'd need to make changes to
    # the code to make them work anyway.

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('thankyou_page_title'),
    ]

    # Serve: method override to "serve" the CustomForm
    def serve(self, request):
        username = None
        if request.user.is_authenticated:
            username = request.user.username

        if request.method == 'POST':
            # If the method is POST, validate the data and perform a save() == INSERT VALUE INTO
            form = form_orchestrator(user_lab=request.session['lab_selected'], request=request.POST)
            if form.is_valid():
                # BEWARE: This is a modelForm and not a object/model, "save" do not have some arguments of the same method, like using=db_tag
                # to work with a normal django object insert a line: data = form.save(commit=False) and then data is a basic model: e.g., you can use data.save(using=external_generic_db)
                # In our example the routing takes care of the external db save
                data = form.save(commit=False)
                data.datausername = username
                data.save()
    
                return render(request, 'home/thank_you_page.html', {
                    'page': self,
                    # We pass the data to the thank you page, data.datavarchar and data.dataint!
                    'data': data,
                })
        else:
            # If the method is not POST (so GET mostly), put the CustomForm in form and then...
            form = form_orchestrator(user_lab=request.session['lab_selected'], request=None)

        # return the form page, with the form as data.
        return render(request, 'home/form_page.html', {
            'page': self,
            'form': form,
        })

class SwitchLabPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def serve(self, request):
        if request.user.is_authenticated:
            username = request.user.username

        if request.method == 'POST':
            # If the method is POST, validate the data and perform a save() == INSERT VALUE INTO
            form = LabSwitchForm(data=request.POST, user_labs=request.user.groups.all())
            if form.is_valid():
                # BEWARE: This is a modelForm and not a object/model, "save" do not have some arguments of the same method, like using=db_tag
                # to work with a normal django object insert a line: data = form.save(commit=False) and then data is a basic model: e.g., you can use data.save(using=external_generic_db)
                # In our example the routing takes care of the external db save
                laboratory = form.cleaned_data.get('lab_selected')
                request.session["lab_selected"] = laboratory
                next = request.POST.get("next", "/")
                return redirect(next)

        else:
            form = LabSwitchForm(user_labs=request.user.groups.all())
            
        renderPage = render(request, 'switch_lab.html', {
                'page': self,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'data': form,
            })
        return renderPage

