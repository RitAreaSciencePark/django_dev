from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission
from django.conf import settings
from django.shortcuts import render
from django.db import connections

class HomePage(Page):
    image = models.ForeignKey("wagtailimages.Image",
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name="+",
                              help_text="Homepage image",
                              )
    introduction_text = models.CharField(
        blank=True,
        max_length=255, help_text="Write an introduction to the site"
    )
    another_text = models.CharField(
        blank=True,
        max_length=255,
        help_text="Another Text!"
    )
    a_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="a link",
        help_text = "Insert a link",
    )

    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("introduction_text"),
            FieldPanel("another_text"),
            FieldPanel("a_link"),
        ]),
        FieldPanel('body')
    ]

class CustomFormData(models.Model):
    data0 = models.CharField(max_length=255)
    data1 = models.CharField(max_length=255)


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

    def serve(self, request):
        from home.forms import CustomForm

        if request.method == 'POST':
            form = CustomForm(request.POST)
            if form.is_valid():
                data = form.save()
                return render(request, 'home/thankyou.html', {
                    'page': self,
                    'data': data,
                })
        else:
            form = CustomForm()

        return render(request, 'home/suggest.html', {
            'page': self,
            'form': form,
        })

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def get_data_fields(self):
        data_fields = [
            ('username', 'Username'),
        ]
        data_fields += super().get_data_fields()

        return data_fields

    def get_submission_class(self):
        return CustomFormSubmission

    def process_form_submission(self, form):
        print(form.user)
        print(form.cleaned_data['this_is_the_first_item'])
        with connections["formrepo"].cursor() as cursor:
            cursor.execute("INSERT INTO easyDMPTestTable (username, data1) VALUES ('{}','{}')".format(form.user, form.cleaned_data['this_is_the_first_item'][0]))

        return self.get_submission_class().objects.create(
            form_data=form.cleaned_data,
            page=self, user=form.user
        )
    def serve(self, request, *args, **kwargs):
        with connections["formrepo"].cursor() as cursor:
            cursor.execute("SELECT * FROM easyDMPTestTable WHERE username = '{}'".format(request.user))
            if(cursor.rowcount>0):
                print("Another user with the name: {} has submitted the form".format(request.user))
                return render(request,
                self.template,
                self.get_context(request)
            )

        return super().serve(request, *args, **kwargs)

class CustomFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_data(self):
        form_data = super().get_data()
        form_data.update({
            'username': self.user.username,
        })

        return form_data
    