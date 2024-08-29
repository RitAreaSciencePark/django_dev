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
from django import forms

from django.contrib.auth.models import User

from .forms import form_orchestrator, LabSwitchForm, DMPform, UserDataForm, ProposalSubmissionForm, SRSubmissionForm, AddNewLabForm, SRForSampleForm#, LageSamplesForm, LameSamplesForm

from PRP_CDM_app.models import labDMP, Administration, Users, Proposals, ServiceRequests, Laboratories, Samples, LageSamples, LameSamples
from django.template.loader import render_to_string

from os import listdir
from os.path import isfile,join,dirname

from uuid import uuid4
from PRP_CDM_app.reports import ReportDefinition
from django.forms.models import model_to_dict

from PRP_CDM_app.code_generation import sr_id_generation, proposal_id_generation, sample_id_generation

from .tables import ProposalsTable,ServiceRequestTable,SamplesTable
from django_tables2.config import RequestConfig


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
            forms = form_orchestrator(user_lab=request.session['lab_selected'], request=request.POST, filerequest=request.FILES)
            
            for form in forms:
                if not form.is_valid():
                    # BEWARE: This is a modelForm and not a object/model, "save" do not have some arguments of the same method, like using=db_tag
                    # to work with a normal django object insert a line: data = form.save(commit=False) and then data is a basic model: e.g., you can use data.save(using=external_generic_db)
                    # In our example the routing takes care of the external db save
                    return render(request, 'home/error_page.html', {
                        'page': self,
                        # We pass the data to the thank you page, data.datavarchar and data.dataint!
                        'errors': form.errors.values, # TODO: improve this
                    })
                
            sr_id = sr_id_generation()
            # sample_id = sample_id_generation()

            for form in forms:
                    data = form.save(commit=False)
                    data.sr_id = sr_id
                    data.user_id = username
                    data.lab_id = request.session["lab_selected"]
                    data.save()
        
            return render(request, 'home/thank_you_page.html', {
                        'page': self,
                        # We pass the data to the thank you page, data.datavarchar and data.dataint!
                        'data': data,
                    })
        else:
            # If the method is not POST (so GET mostly), put the CustomForm in form and then...
            try:
                if(request.session['lab_selected'] is None):
                    next = request.POST.get("next", "/switch-laboratory")
                    return redirect(next)
                else:
                    forms = form_orchestrator(user_lab=request.session['lab_selected'], request=None, filerequest=None)
            except KeyError:
                next = request.POST.get("next", "/switch-laboratory")
                return redirect(next)
        
        pageDict = {
            'page': self,
            'lab': request.session['lab_selected'],
            }
        
        for form in forms:
            pageDict[form.Meta.model.__name__]=form
            
        pageDict['forms'] = forms
        formlist =[]
        # return the form page, with the form as data.
        # TODO: while using settings is correct, create/find another softcoded var!!
        try:
            home_path = settings.PROJECT_DIR[:len(settings.PROJECT_DIR)-7]
            abs_path = join(home_path,"home/templates/home/forms/")
            formlist = [f for f in listdir(abs_path)]
        except Exception as e:
            e # TODO: properly catch this

        for formTemplate in formlist:
            if pageDict['lab'].lower() in formTemplate:
                return render(request, 'home/forms/' + formTemplate, pageDict)
        return render(request, 'home/generic_form_page.html', pageDict)

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
                try:
                    return redirect(request.session["return_page"])  # TODO: Not working as intended
                except:
                    return redirect('/')
        else:
            request.session["return_page"] = request.META['HTTP_REFERER']
            form = LabSwitchForm(user_labs=request.user.groups.all())
            
        renderPage = render(request, 'switch_lab.html', {
                'page': self,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'data': form,
            })
        return renderPage

class DMPPage(Page):
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

    def serve(self,request):
        if request.user.is_authenticated:
            username = request.user.username
        
        try:
            if(request.session['lab_selected'] is None):
                request.session["return_page"] = request.META['HTTP_REFERER']
                next = request.POST.get("next", "/switch-laboratory")
                return redirect(next)
        except KeyError:
            request.session["return_page"] = request.META['HTTP_REFERER']
            next = request.POST.get("next", "/switch-laboratory")
            return redirect(next)

        if request.method == 'POST':
            # If the method is POST, validate the data and perform a save() == INSERT VALUE INTO
            form = DMPform(data=request.POST)
            if form.is_valid():
                # BEWARE: This is a modelForm and not a object/model, "save" do not have some arguments of the same method, like using=db_tag
                # to work with a normal django object insert a line: data = form.save(commit=False) and then data is a basic model: e.g., you can use data.save(using=external_generic_db)
                # In our example the routing takes care of the external db save
                data = form.save(commit=False)
                data.lab_id = request.session["lab_selected"]
                data.user_id = username
                data.save()
                return render(request, 'home/labdmp_page.html', {
                    'page': self,
                    # We pass the data to the thank you page, data.datavarchar and data.dataint!
                    'data': form,
                    'lab': request.session['lab_selected'],
                })
            else:
                return render(request, 'home/error_page.html', {
                        'page': self,
                        # We pass the data to the thank you page, data.datavarchar and data.dataint!
                        'errors': form.errors.values, # TODO: improve this
                    })

        else:
            try:
                if labDMP.objects.get(pk=request.session["lab_selected"]) is not None:
                    form = DMPform(instance=labDMP.objects.get(pk=request.session["lab_selected"]))
                else:
                    form = DMPform()
            except Exception as e: # TODO Properly catch this
                form = DMPform()

        return render(request, 'home/labdmp_page.html', {
                'page': self,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'data': form,
                'lab': request.session['lab_selected'],
            })

class DMPSearchPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    def serve(self,request):
        if request.user.is_authenticated:
            username = request.user.username
        
        try: # TODO: optimize this
            if(request.session['lab_selected'] is None):
                request.session["return_page"] = request.META['HTTP_REFERER']
                next = request.POST.get("next", "/switch-laboratory")
                return redirect(next)
        except KeyError:
            request.session["return_page"] = request.META['HTTP_REFERER']
            next = request.POST.get("next", "/switch-laboratory")
            return redirect(next)
        
        data = Administration.objects.filter(lab_id=request.session['lab_selected'])
        return render(request, 'home/dmp_search.html', {
            'page': self,
            'data': data,
        })

class DMPViewPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    def serve(self,request):
        if request.user.is_authenticated:
            username = request.user.username
        
        try: # TODO: optimize this
            if(request.session['lab_selected'] is None):
                request.session["return_page"] = request.META['HTTP_REFERER']
                next = request.POST.get("next", "/switch-laboratory")
                return redirect(next)
        except KeyError: # TODO: Fix the HTTP_REFERER Not present! 
            request.session["return_page"] = request.META['HTTP_REFERER']
            next = request.POST.get("next", "/switch-laboratory")
            return redirect(next)
        
        def pkSelection(modelTable, pk):
            return modelTable.objects.get(pk=pk)
        
        def reportOrchestrator(user_lab):
        # lablist = [labform for labform in dir(FORMS()) if not labform.startswith("__")]
            if user_lab is None:
                return None # TODO manage this
            else:
                # this block checks the class names into FormsDefinition to create the forms
                reportClass = getattr(ReportDefinition,user_lab.title() + "Report")
                return reportClass.content
        
        reportList = []
        if request.method == 'POST':
            for report in reportOrchestrator(user_lab=request.session['lab_selected']):
                reportList.append(pkSelection(modelTable=report, pk=request.POST.get('sr_id')))
                pass
        else:
            try:
                for report in reportOrchestrator(user_lab=request.session['lab_selected']):
                    reportList.append(pkSelection(modelTable=report, pk=request.session["sr_id"]))
            except:
                return redirect('/')

        pageDict = {
            'page': self,
            'lab': request.session['lab_selected'],
            }

        reports = {}
        for fields in reportList:
            pageDict[type(fields).__name__] = (model_to_dict(fields))
            reports[type(fields).__name__] = (model_to_dict(fields))
        
        pageDict['reports'] = reports

        # return the form page, with the form as data.
        # TODO: while using settings is correct, create/find another softcoded var!!
        try:
            home_path = settings.PROJECT_DIR[:len(settings.PROJECT_DIR)-7]
            abs_path = join(home_path,"home/templates/home/reports/")
            reportlist = [f for f in listdir(abs_path)]
        except Exception as e:
            e # TODO: properly catch this

        for reportTemplate in reportlist:
            if pageDict['lab'].lower() in reportTemplate:
                return render(request, 'home/reports/' + reportTemplate, pageDict)
        return render(request, 'home/generic_dmp_view.html', pageDict)


class UserDataPage(Page): # USER DATA
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

    def serve(self,request):
        if request.user.is_authenticated:
            username = request.user.username

        if request.method == 'POST':
            # If the method is POST, validate the data and perform a save() == INSERT VALUE INTO
            form = UserDataForm(data=request.POST)
            if form.is_valid():
                # BEWARE: This is a modelForm and not a object/model, "save" do not have some arguments of the same method, like using=db_tag
                # to work with a normal django object insert a line: data = form.save(commit=False) and then data is a basic model: e.g., you can use data.save(using=external_generic_db)
                # In our example the routing takes care of the external db save
                data = form.save(commit=False)
                #data.lab_id = request.session["lab_selected"]
                data.user_id = username
                data.save()
                return render(request, 'home/user_data_page.html', {
                    'page': self,
                    # We pass the data to the thank you page, data.datavarchar and data.dataint!
                    'data': form,
                })
            else:
                debug = form.errors
                return render(request, 'home/error_page.html', {
                        'page': self,
                        # We pass the data to the thank you page, data.datavarchar and data.dataint!
                        'errors': form.errors.values, # TODO: improve this
                    })

        else:
            #form = UserRegistrationForm()
            try:
                if Users.objects.get(pk=username) is not None:
                    form = UserDataForm(instance=Users.objects.get(pk=username))
                else:
                    form = UserDataForm()
            except Exception as e: # TODO Properly catch this
                form = UserDataForm()

            
        return render(request, 'home/user_data_page.html', {
                'page': self,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'data': form,
            })





class ProposalSubmissionPage(Page): # USER DATA
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

    def serve(self,request):
        if request.user.is_authenticated:
            username = request.user.username

        if request.method == 'POST':
            # If the method is POST, validate the data and perform a save() == INSERT VALUE INTO
            form = ProposalSubmissionForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                # BEWARE: This is a modelForm and not a object/model, "save" do not have some arguments of the same method, like using=db_tag
                # to work with a normal django object insert a line: data = form.save(commit=False) and then data is a basic model: e.g., you can use data.save(using=external_generic_db)
                # In our example the routing takes care of the external db save
                data = form.save(commit=False)
                data.proposal_id = proposal_id_generation()
                data.proposal_status = 'Submitted'
                if Users.objects.get(pk=username) is not None:
                    data.user_id = Users.objects.get(pk=username)
                
                #debug = data.proposal_filename

                data.save()
                return render(request, 'home/thank_you_proposal_page.html', {
                    'page': self,
                    # We pass the data to the thank you page, data.datavarchar and data.dataint!
                    'data': data,
                })
            else:
                #debug = form.errors
                return render(request, 'home/error_page.html', {
                        'page': self,
                        # We pass the data to the thank you page, data.datavarchar and data.dataint!
                        'errors': form.errors.values, # TODO: improve this
                    })

        else:
            #form = UserRegistrationForm()
            try:
                if Proposals.objects.get(pk=username) is not None:
                    form = ProposalSubmissionForm(instance=Proposals.objects.get(pk=username))
                else:
                    form = ProposalSubmissionForm()
            except Exception as e: # TODO Properly catch this
                form = ProposalSubmissionForm()


        return render(request, 'home/proposal_submission_page.html', {
                'page': self,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'data': form,
            })



class ProposalListPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    def serve(self,request):
        if request.user.is_authenticated:
            username = request.user.username
        if "filter" in request.GET:
            filter = request.GET.get("filter","")
        else:
            filter = ""
            request.GET = request.GET.copy()
            request.GET["filter"]= ""

        if request.method == 'POST':
            filter = request.POST.get("filter","")
            request.GET = request.GET.copy()
            request.GET["filter"] = request.POST.get("filter","")
        

        data = Proposals.objects.filter(user_id_id=request.user.username)
        data = data.filter(proposal_id__contains = filter)
        table = ProposalsTable(data)
        RequestConfig(request).configure(table)

        table.paginate(page=request.GET.get("page",1), per_page=25)
        return render(request, 'home/proposal_list.html', {
            'page': self,
            'table': table,
        })
    
class AddNewLabPage(Page): # USER DATA
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

    def serve(self,request):
        if request.method == 'POST':
            # If the method is POST, validate the data and perform a save() == INSERT VALUE INTO
            form = AddNewLabForm(data=request.POST)
            if form.is_valid():
                data = form.save()
                return render(request, 'home/thank_you_page.html', {
                    'page': self,
                    # We pass the data to the thank you page, data.datavarchar and data.dataint!
                    'data': data,
                })
            else:
                #debug = form.errors
                return render(request, 'home/error_page.html', {
                        'page': self,
                        # We pass the data to the thank you page, data.datavarchar and data.dataint!
                        'errors': form.errors.values, # TODO: improve this
                    })

        else:
            #form = UserRegistrationForm()
            try:
                if Laboratories.objects.get() is not None:
                    form = AddNewLabForm()
                else:
                    form = AddNewLabForm()
            except Exception as e: # TODO Properly catch this
                form = AddNewLabForm()


        return render(request, 'home/add_new_lab_page.html', {
                'page': self,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'data': form,
            })
    



class SRSubmissionPage(Page):
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
        max_length=255, help_text="Title text to use for the 'thank you' page")
    # Note that there's nothing here for specifying the actual form fields -
    # those are still defined in forms.py. There's no benefit to making these
    # editable within the Wagtail admin, since you'd need to make changes to
    # the code to make them work anyway.

    # drop down

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        #FieldPanel('Proposals', widget=forms.Select(choices=Proposals.objects.all().order_by('proposal_id'))),
        FieldPanel('thankyou_page_title'),
    ]

    def serve(self,request):
        if request.user.is_authenticated:
            username = request.user.username

        if "filter" in request.GET:
            filter = request.GET.get("filter","")
        else:
            filter = ""
            request.GET = request.GET.copy()
            request.GET["filter"]= ""

        if request.method == 'POST':
            filter = request.POST.get("filter","")
            request.GET = request.GET.copy()
            request.GET["filter"] = request.POST.get("filter","")
        

        data = Proposals.objects.filter(user_id=username)
        data = data.filter(proposal_id__contains = filter)
        table = ProposalsTable(data)
        RequestConfig(request).configure(table)
        table.paginate(page=request.GET.get("page",1), per_page=3)
        if request.method == 'POST':
            # If the method is POST, validate the data and perform a save() == INSERT VALUE INTO
            form = SRSubmissionForm(data=request.POST, user=username)
            if form.is_valid():
                # BEWARE: This is a modelForm and not a object/model, "save" do not have some arguments of the same method, like using=db_tag
                # to work with a normal django object insert a line: data = form.save(commit=False) and then data is a basic model: e.g., you can use data.save(using=external_generic_db)
                # In our example the routing takes care of the external db save
                data = form.save(commit=False)
                data.sr_id = sr_id_generation()
                data.sr_status = 'Submitted'
                
                #debug = data.proposal_filename

                data.save()
                return render(request, 'home/thank_you_sr_page.html', {
                    'page': self,
                    # We pass the data to the thank you page, data.datavarchar and data.dataint!
                    'data': data,
                })
            else:
                #debug = form.errors
                return render(request, 'home/error_page.html', {
                        'page': self,
                        # We pass the data to the thank you page, data.datavarchar and data.dataint!
                        'errors': form.errors.values, # TODO: improve this
                    })

        else:
            #form = UserRegistrationForm()
            try:
                if ServiceRequests.objects.get(pk=username) is not None:
                    form = SRSubmissionForm(instance=ServiceRequests.objects.get(pk=username), user=username)
                else:
                    form = SRSubmissionForm(user=username)
            except Exception as e: # TODO Properly catch this
                form = SRSubmissionForm(user=username)


        return render(request, 'home/sr_submission_page.html', {
                'page': self,
                'table': table,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'data': form,
            })

class SRForSamplePage(Page):

    def serve(self, request):
        if request.user.is_authenticated:
            username = request.user.username
        
        if "filter" in request.GET:
            filter = request.GET.get("filter","")
        else:
            filter = ""
            request.GET = request.GET.copy()
            request.GET["filter"]= ""

        if request.method == 'POST':
            filter = request.POST.get("filter","")
            request.GET = request.GET.copy()
            request.GET["filter"] = request.POST.get("filter","")
        

        data = ServiceRequests.objects.filter(lab_id=request.session.get('lab_selected'))
        data = data.filter(sr_id__contains = filter)
        table = ServiceRequestTable(data)
        RequestConfig(request).configure(table)

        table.paginate(page=request.GET.get("page",1), per_page=25)
        return render(request, 'home/lab_sample_page.html', {
            'page': self,
            'table': table,
        })

class SamplePage(Page):
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
    max_length=255, help_text="Title text to use for the 'thank you' page")
       
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('thankyou_page_title'),
        ]
    
    def serve(self, request):
        if 'sr_id' in request.GET:
            sr_id = request.GET.get('sr_id')
        elif request.method == 'POST':
            sr_id = request.POST.get('sr_id')
        else:
            return redirect("/sample-entry")
        sr = ServiceRequests.objects.get(sr_id=sr_id)
        lab = sr.lab_id

        if request.method == 'POST':
            
            forms = form_orchestrator(user_lab=lab.lab_id, request=request.POST, filerequest=request.FILES)

            for form in forms:
                if not form.is_valid():
                    return render(request, 'home/error_page.html', {
                        'page': self,
                        'errors': form.errors.values, # TODO: improve this
                    })
                else:
                    data = form.save(commit=False)
                    data.sr_id = sr
                    data.sample_id = sample_id_generation()
                    data.lab_id = lab
                    data.sample_status = 'Submitted'
                    data.save()
            return render(request, 'home/thank_you_page.html', {
                'page': self,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'data': data,
                })

        else:
            forms = form_orchestrator(user_lab=lab.lab_id, request=None, filerequest=None)
        
        pageDict = {
            'page': self,
            'lab': lab.lab_id,
            'sr_id': sr_id,
            }
        
        for form in forms:
            pageDict[form.Meta.model.__name__] = form
            
        pageDict['forms'] = forms
        formlist =[]
        # return the form page, with the form as data.
        # TODO: while using settings is correct, create/find another softcoded var!!
        try:
            home_path = settings.PROJECT_DIR[:len(settings.PROJECT_DIR)-7]
            abs_path = join(home_path,"home/templates/home/forms/")
            formlist = [f for f in listdir(abs_path)]
        except Exception as e:
            e # TODO: properly catch this

        for formTemplate in formlist:
            if pageDict['lab'].lower() in formTemplate:
                return render(request, 'home/forms/' + formTemplate, pageDict)
        return render(request, 'home/generic_form_page.html', pageDict)
    
class SampleListPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    def serve(self,request):
        if request.user.is_authenticated:
            username = request.user.username
        if "filter" in request.GET:
            filter = request.GET.get("filter","")
        else:
            filter = ""
            request.GET = request.GET.copy()
            request.GET["filter"]= ""

        if request.method == 'POST':
            filter = request.POST.get("filter","")
            request.GET = request.GET.copy()
            request.GET["filter"] = request.POST.get("filter","")
        

        data = Samples.objects.filter(lab_id=request.session.get('lab_selected'))
        data = data.filter(sample_id__contains = filter)
        table = SamplesTable(data)
        RequestConfig(request).configure(table)

        table.paginate(page=request.GET.get("page",1), per_page=25)
        return render(request, 'home/proposal_list.html', {
            'page': self,
            'table': table,
        })