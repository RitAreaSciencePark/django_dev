from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission
from django.conf import settings
from django.shortcuts import render
from django.db import connections

# This is the model of the HomePage, extending "Page"
class HomePage(Page):
    # Foreign key is used to link the wagtailimages.Image app and the template
    image = models.ForeignKey("wagtailimages.Image",
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name="+",
                              help_text="Homepage image",
                              )
    # A simple Charfield
    introduction_text = models.CharField(
        blank=True,
        max_length=255, help_text="Write an introduction to the site"
    )

    # An internal link to a the app wagtailcore.Page
    a_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="a link",
        help_text = "Insert a link",
    )

    # A Charfield with RichText
    body = RichTextField(blank=True)

    # Here are defined all the panels
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("introduction_text"),
            FieldPanel("a_link"),
        ]),
        FieldPanel('body')
    ]

class CustomFormData(models.Model):
    datavarchar = models.CharField(max_length=255)
    dataint = models.IntegerField()

    class Meta:
        db_table='customformdata'

class CustomFormPage(Page):
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
        from home.forms import CustomForm
        username = None
        if request.user.is_authenticated:
            username = request.user.username

        if request.method == 'POST':
            # If the method is POST, validate the data and perform a save() == INSERT VALUE INTO
            form = CustomForm(request.POST)
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
            form = CustomForm()

        # return the form page, with the form as data.
        return render(request, 'home/form_page.html', {
            'page': self,
            'form': form,
        })

    
