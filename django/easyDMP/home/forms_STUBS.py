from django import forms
# This import point to the external app schema!
from PRP_CDM_app.models import CustomAppModel

# TODO: STUB
class CustomForm(forms.ModelForm):
    
    # see https://docs.djangoproject.com/en/1.9/topics/forms/ for more complex example.
    # We are using a ModelForm, it is not mandatory
    class Meta:
        model = CustomAppModel
        fields = ['datavarchar', 'dataint']

# TODO: ALSO A STUB: PUT THIS IN MODEL WHEN THE TIME COMES
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
        from django.easyDMP.home.forms_STUBS import CustomForm
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
