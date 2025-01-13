from django.db import models, connections
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
from django import forms

from django.contrib.auth.models import User, Group

from .forms import form_orchestrator, LabSwitchForm, DMPform, UserDataForm, APITokenForm, ProposalSubmissionForm, SRSubmissionForm, AddNewLabForm, SRForSampleForm#, LageSamplesForm, LameSamplesForm

from PRP_CDM_app.models import labDMP, Administration, Users, Proposals, ServiceRequests, Laboratories, Samples, LageSamples, LameSamples, API_Tokens
from django.template.loader import render_to_string

from os import listdir
from os.path import isfile,join,dirname

from uuid import uuid4
from PRP_CDM_app.reports import ReportDefinition
from django.forms.models import model_to_dict

from PRP_CDM_app.code_generation import sr_id_generation, proposal_id_generation, sample_id_generation

from .tables import ProposalsTable,ServiceRequestTable,SamplesTable
from django_tables2.config import RequestConfig

from django.contrib.auth.models import Group
Group.add_to_class('laboratory', models.BooleanField(default=False))   
from django.core.exceptions import ObjectDoesNotExist

from .decos_elab import Decos_Elab_API
from .decos_jenkins import Decos_Jenkins_API


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

@register_setting
class ApiSettings(BaseGenericSetting):
    # TODO: FIX FOR MULTIPLE LABS!  
    elab_base_url = models.URLField(verbose_name = "elab url", blank=True)
    jenkins_base_url = models.URLField(verbose_name="jenkins url", blank = True)
    
    panels = [
        FieldPanel("elab_base_url"),
        FieldPanel("jenkins_base_url"),
    ]

class HomePage(Page):
    intro = models.CharField(max_length=250, default="")
    body = RichTextField(blank=True)
    content_panels = [
    FieldPanel("title"),
    FieldPanel("intro"),
    FieldPanel("body"),
    ]

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
            try:
                request.session["return_page"] = request.META['HTTP_REFERER']
            except KeyError:
                request.session["return_page"] = "/"
            
            debug = request.user.groups.all()
            if not request.user.groups.all():
                return render(request, 'home/error_page.html', {
                'page': self,
                'errors': {"No assigned laboratory":"The User has no assigned laboratory, contact the administrator."}, # TODO: improve this
                })
            form = LabSwitchForm(user_labs=request.user.groups.all())
            
        renderPage = render(request, 'switch_lab.html', {
                'page': self,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'data': form,
            })
        return renderPage

class UserDataPage(Page):
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
            debug = request.POST
            form_user = UserDataForm(data=request.POST)
            if form_user.is_valid():
                # BEWARE: This is a modelForm and not a object/model, "save" do not have some arguments of the same method, like using=db_tag
                # to work with a normal django object insert a line: data = form.save(commit=False) and then data is a basic model: e.g., you can use data.save(using=external_generic_db)
                # In our example the routing takes care of the external db save
                data = form_user.save(commit=False)
                #data.lab_id = request.session["lab_selected"]
                data.user_id = username
                data.save()
            form_api_tokens = APITokenForm(data=request.POST)
            try:
                if form_api_tokens['laboratory'].data != '':
                    lab = form_api_tokens['laboratory'].data
                    # elab_token = form_api_tokens['elab_token'].data
                    # jenkins_token = form_api_tokens['jenkins_token'].data
                    data = form_api_tokens.save(commit=False)
                    if form_api_tokens.is_valid() and lab != '':
                        api_token_queryset = API_Tokens.objects.filter(laboratory_id = Laboratories.objects.get(pk = lab), user_id = Users.objects.get(pk=username))
                        if api_token_queryset.values().count() > 0:
                            data.id = api_token_queryset.first().id
                            if form_api_tokens['elab_token'].data == '':
                                data.elab_token = api_token_queryset.values('elab_token').first()['elab_token']
                            if form_api_tokens['jenkins_token'].data == '':
                                data.jenkins_token = api_token_queryset.values('jenkins_token').first()['jenkins_token']

                        data.user_id = Users.objects.get(pk=username)
                        data.save()
                        return render(request, 'home/user_data_page.html', {
                        'page': self,
                        # We pass the data to the thank you page, data.datavarchar and data.dataint!
                        'user_data': form_user,
                        'api_token_data': form_api_tokens,
                    })
                else:
                    return render(request, 'home/user_data_page.html', {
                    'page': self,
                    # We pass the data to the thank you page, data.datavarchar and data.dataint!
                    'user_data': form_user,
                    'api_token_data': APITokenForm(),
                })
            except KeyError as e:
                pass
                
            
            else:
                return render(request, 'home/error_page.html', {
                        'page': self,
                        # We pass the data to the thank you page, data.datavarchar and data.dataint!
                        'errors': form.errors, # TODO: improve this
                    })
            
        else:
            #form = UserRegistrationForm()
            try:
                if Users.objects.get(pk=username) is not None:
                    form_user = UserDataForm(instance=Users.objects.get(pk=username))
                else:
                    form_user = UserDataForm()
            except Exception as e: # TODO Properly catch this
                form_user = UserDataForm()

            try:
                if API_Tokens.objects.get(pk=username) is not None:
                    form_api_tokens = APITokenForm(instance=Users.objects.get(pk=username))
                else:
                    form_api_tokens = APITokenForm()
            except Exception as e: # TODO Properly catch this
                form_api_tokens = APITokenForm()

        return render(request, 'home/user_data_page.html', {
                'page': self,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'user_data': form_user,
                'api_token_data': form_api_tokens,
            })

class SamplePage(Page): # EASYDMP / DIMMT?
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
    max_length=255, help_text="Title text to use for the 'thank you' page")
       
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('thankyou_page_title'),
        ]
    
    def serve(self, request):

        if request.user.is_authenticated:
            username = request.user.username

        if "filter" in request.GET:
            filter = request.GET.get("filter","")
        else:
            filter = ""
            request.GET = request.GET.copy()
            request.GET["filter"]= ""

        if request.method == 'POST': #???
            filter = request.POST.get("filter","")
            request.GET = request.GET.copy()
            request.GET["filter"] = request.POST.get("filter","")
        
        if(request.GET.get("sr_id") and request.GET.get("sr_id") != "internal"):
           sr_id = request.GET.get("sr_id")
           sr = ServiceRequests.objects.get(sr_id = sr_id)
        else:
            sr_id = "internal"
            sr = None

        try:
            if(request.session['lab_selected'] is None):
                request.session["return_page"] = request.META['HTTP_REFERER']
                next = request.POST.get("next", "/switch-laboratory")
                return redirect(next)
            else:
                lab = Laboratories.objects.get(pk = request.session['lab_selected'])
        except KeyError:
            request.session["return_page"] = request.META['HTTP_REFERER']
            next = request.POST.get("next", "/switch-laboratory")
            return redirect(next)
        
        try:
            elab_token = API_Tokens.objects.filter(user_id=username, laboratory_id = lab).values("elab_token").first()['elab_token']
            elab_api = Decos_Elab_API('https://prp-electronic-lab.areasciencepark.it/', elab_token)
        except Exception as e: # TODO: catch and manage this
            print(f"error on elab_api: {e}") 

        if request.method == 'POST':

            forms = form_orchestrator(user_lab=lab.lab_id, request=request.POST, filerequest=request.FILES)

            for form in forms:
                if not form.is_valid():
                    return render(request, 'home/error_page.html', {
                        'page': self,
                        'errors': form.errors, # TODO: improve this
                    })
                else:
                    data = form.save(commit=False)
                    if(request.POST.get("sr_id_hidden") and (request.POST.get("sr_id_hidden") != 'internal')):
                        data.sr_id = ServiceRequests.objects.get(pk=request.POST.get("sr_id_hidden"))
                    data.sample_id = sample_id_generation(data.sr_id)
                    data.lab_id = lab
                    data.sample_status = 'Submitted'
                    data.save()
                    # TODO: ElabFTWAPI!
                    elab_api.create_new_decos_experiment(lab=lab,username=username,experiment_info=data)
                    
            return render(request, 'home/thank_you_page.html', {
                'page': self,
                # We pass the data to the thank you page, data.datavarchar and data.dataint!
                'data': data,
                })

        else:
            forms = form_orchestrator(user_lab=lab.lab_id, request=None, filerequest=None)
        
        dataQuery = ServiceRequests.objects.filter(lab_id=lab.lab_id)
        dataQuery = dataQuery.filter(sr_id__contains = filter)
        table = ServiceRequestTable(dataQuery)
        RequestConfig(request).configure(table)

        table.paginate(page=request.GET.get("page",1), per_page=25)

        pageDict = {
            'page': self,
            'lab': lab.lab_id,
            'sr_id': sr_id,
            'table': table,
            }
        
        for form in forms:
            pageDict[form.Meta.model.__name__] = form
            
        pageDict['forms'] = forms
        formlist =[]
        # return the form page, with the form as data.
        # TODO: while using settings is correct, create/find another softcoded var!!
        try:
            home_path = settings.BASE_DIR
            abs_path = join(home_path,"home/templates/home/forms/")
            formlist = [f for f in listdir(abs_path)]
        except Exception as e:
            e # TODO: properly catch this

        for formTemplate in formlist:
            if pageDict['lab'].lower() in formTemplate:
                return render(request, 'home/forms/' + formTemplate, pageDict)
        return render(request, 'home/generic_form_page.html', pageDict)

class SampleListPage(Page): # EASYDMP
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    def serve(self,request):
        if request.user.is_authenticated:
            username = request.user.username
        
        try:
            if(request.session['lab_selected'] is None):
                request.session["return_page"] = request.META['HTTP_REFERER']
                next = request.POST.get("next", "/switch-laboratory")
                return redirect(next)
            else:
                lab = Laboratories.objects.get(pk = request.session['lab_selected'])
        except KeyError:
            request.session["return_page"] = request.META['HTTP_REFERER']
            next = request.POST.get("next", "/switch-laboratory")
            return redirect(next)

        try: # TODO: MAKE IT NOT HARDCODED!
            jenkins_token = API_Tokens.objects.filter(user_id=username, laboratory_id = lab).values("jenkins_token").first()['jenkins_token']
            credentials = (username, jenkins_token)
            # 'http://localhost:9000/' or jenkins-test
            jenkins_api = Decos_Jenkins_API('http://jenkins-test:8080/', credentials)
            sample_id_list = jenkins_api.get_sample_list(f"test_Folder/job/folderList")
            sample_list = []
            for sample_id, sample_location in sample_id_list:
                try:
                    sample = (Samples.objects.get(pk = sample_id))
                    sample.sample_location = "/"+sample_location
                    sample.save()
                except Samples.DoesNotExist as e:
                    print("Debug: {e}")

        except Exception as e: # TODO: catch and manage this
            print(f"error on jenkins_api: {e}") 
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
        return render(request, 'home/proposal_list.html', { # TODO: WHY PROPOSALS, WHYY!!!?! 
            'page': self,
            'table': table,
        })

class DMPPage(Page): # EASYDMP
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
                        'errors': form.errors, # TODO: improve this
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

class DMPSearchPage(Page): # EASYDMP
    pass

class DMPViewPage(Page): #EASYDMP
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
            home_path = settings.BASE_DIR
            abs_path = join(home_path,"home/templates/home/reports/")
            reportlist = [f for f in listdir(abs_path)]
        except Exception as e:
            e # TODO: properly catch this

        for reportTemplate in reportlist:
            if pageDict['lab'].lower() in reportTemplate:
                return render(request, 'home/reports/' + reportTemplate, pageDict)
        return render(request, 'home/generic_dmp_view.html', pageDict)

class ProposalSubmissionPage(Page): # USER DATA DIMMT
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
                data.proposal_id = proposal_id_generation(Users.objects.get(pk=username).affiliation)
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
                        'errors': form.errors, # TODO: improve this
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

class ProposalListPage(Page): # DIMMT
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

class ServiceRequestSubmissionPage(Page): # DIMMT
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
            request.GET["filter"]= filter

        if request.method == 'POST':
            filter = request.POST.get("filter","")
            request.GET = request.GET.copy()
            request.GET["filter"] = request.POST.get("filter","")
        

        dataQuery = Proposals.objects.filter(user_id=username)
        dataQuery = dataQuery.filter(proposal_id__contains = filter)
        table = ProposalsTable(dataQuery)
        RequestConfig(request).configure(table)
        table.paginate(page=request.GET.get("page",1), per_page=25)
        if request.method == 'POST':
            # If the method is POST, validate the data and perform a save() == INSERT VALUE INTO
            form = SRSubmissionForm(data=request.POST, user=username)
            if form.is_valid():
                # BEWARE: This is a modelForm and not a object/model, "save" do not have some arguments of the same method, like using=db_tag
                # to work with a normal django object insert a line: data = form.save(commit=False) and then data is a basic model: e.g., you can use data.save(using=external_generic_db)
                # In our example the routing takes care of the external db save
                data = form.save(commit=False)
                data.proposal_id = Proposals.objects.get(pk=request.POST.get('proposalId'))
                data.sr_id = sr_id_generation(proposal=data.proposal_id, lab=form.cleaned_data["lab_id"])
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
                        'errors': form.errors, # TODO: improve this
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
                # keep the selection form open or not ("true" or "false")
            })

