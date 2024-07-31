from django.db import models
# This apps is reserved to create the models of our external database schema
# through django ORM
from django import forms
from uuid import uuid4
from .fields import MultiChoicheAndOtherWidget, BooleanIfWhat

# NOTE: For "multiple choices + free text fields"
# in this version they must be declared like this:
#    test_choices = (
#        ("A","A"),
#        ("B","B"),
#    )
#    test = models.CharField(blank=True)
#    widgets = {"test": MultiChoicheAndOtherWidget(choices=test_choices),}
# NOTE: If multiple choices without free text field, use:
#     test = models.CharField(choices=test_choices)
 

class Users(models.Model):
    widgets = {}
    user_id = models.CharField(max_length=37, primary_key=True)
    name_surname = models.CharField(max_length=50)
    email = models.CharField(max_length=128)
    affiliation = models.CharField(max_length=128)
    gender_choices = (
        ("male","male"),
        ("female","female"),
        ("other","other"),
    )
    gender = models.CharField(blank=True)
    widgets["gender"] = MultiChoicheAndOtherWidget(choices=gender_choices)
    legal_status_choices = (
        ("OTH","male"),
        ("PRV","female"),
        ("RES","other"),
        ("SME","other"),
        ("UNI","other"),
    )
    legal_status = models.CharField(blank=True)
    widgets["legal_status"] = MultiChoicheAndOtherWidget(choices=legal_status_choices)
    research_role_choices = (("senior scientist","senior scientist"),
        ("phd student","phd student"),
        ("professor / scientific coordinator","professor / scientific coordinator"),
        ("scientist","scientist"),
        ("manager","manager"),
        ("degree student","degree student"),
        ("post-doc","post-doc"),
        ("technician","technician"),
        ("other","other"),
    )
    research_role = models.CharField(blank=True)
    widgets["research_role"] = MultiChoicheAndOtherWidget(choices=research_role_choices)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'users'.lower()


class ServiceRequests(models.Model):
    widgets = {}
    sr_id = models.CharField(max_length=37, primary_key=True)
    user_id = models.CharField(max_length=37) # FK table users
    lab_id = models.CharField(max_length=37) # FK table laboratories
    sr_status = models.CharField(default='draft')
    sr_feasibility_choices = (("feasible","feasible"),
        ("not feasible","not feasible"),
        ("feasible with reservations","feasible with reservations"),
    )
    sr_feasibility = models.CharField(blank=True)
    widgets["sr_feasibility"] = MultiChoicheAndOtherWidget(choices=sr_feasibility_choices)
    exp_description = models.TextField(max_length=500, blank=True)
    output_delivery_date = models.DateField(blank=True)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'service_requests'.lower()


class Laboratories(models.Model):
    lab_id = models.CharField(max_length=37, primary_key=True)
    description = models.CharField(max_length=50)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'laboratories'.lower()


class Samples(models.Model):
    widgets = {}
    sample_id = models.CharField(max_length=37, primary_key=True)
    sr_id = models.CharField(max_length=37) # FK table service_requests
    type_choices = (
        ("DNA","DNA"),
        ("RNA","RNA"),
        ("pellet","pellet"),
        ("biopsy","biopsy"),
    )
    type = models.CharField(blank=True)
    widgets["type"] = MultiChoicheAndOtherWidget(choices=type_choices)
    sample_description = models.TextField(max_length=500, blank=True)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'samples'.lower()

class LageSamples(models.Model):
    widgets = {}
    sample_id = models.CharField(max_length=37, primary_key=True) # also FK table samples
    is_volume_in_ul = models.CharField(blank=True)
    widgets["is_volume_in_ul"] = BooleanIfWhat(yes_or_no=False)
    is_buffer_used = models.CharField(blank=True)
    widgets["is_buffer_used"] = BooleanIfWhat(yes_or_no=False)
    is_quality = models.CharField(blank=True)
    widgets["is_quality"] = BooleanIfWhat(yes_or_no=False)
    sample_date_of_delivery = models.DateField()
    sample_back = models.BooleanField()
    reagents_provided_by_client = models.BooleanField()
    reagents_date_of_delivery = models.DateField(blank=True)
    
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'uploads/{0}/{1}/{2}'.format(instance.datausername, instance.uuid, filename)

    sample_sheet_filename = models.FileField(blank=True, upload_to=user_directory_path)

    additional_filename = models.FileField(blank=True, upload_to=user_directory_path)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'lage_samples'.lower()


class Instruments(models.Model):
    instrument_id = models.CharField(max_length=37, primary_key=True)
    vendor = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'instruments'.lower()


class Techniques(models.Model):
    technique_id = models.CharField(max_length=37, primary_key=True)
    technique_name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'techniques'.lower()


class InstrumentXTechnique(models.Model):
    x_id = models.CharField(max_length=37, primary_key=True)
    instrument_id = models.CharField(max_length=37) # FK table instruments
    technique_id = models.CharField(max_length=37) # FK table techniques

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'instrument_x_technique'.lower()

class LabXInstrument(models.Model):
    x_id = models.CharField(max_length=37, primary_key=True)
    lab_id = models.CharField(max_length=37) # FK table laboratories
    instrument_id = models.CharField(max_length=37) # FK table instruments

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'lab_x_instrument'.lower()

class Steps(models.Model):
    widgets = {}
    step_id = models.CharField(max_length=37, primary_key=True)
    sr_id = models.CharField(max_length=37) # FK table service_requests
    instrument_id = models.CharField(max_length=37) # FK table instruments
    technique_id = models.CharField(max_length=37) # FK table techniques
    assigned_uoa = models.IntegerField()
    performed_uoa = models.IntegerField(default = 0)
    eff_sample_date_of_delivery = models.DateField()
    eff_reagents_date_of_delivery = models.DateField()
    sample_quality_choices = (
        ("good","good"),
        ("not good","not good"),
        ("partially good","partially good"),
    )
    sample_quality = models.CharField(blank=True)
    widgets["sample_quality"] = MultiChoicheAndOtherWidget(choices=sample_quality_choices)
    sample_quality_description = models.TextField(max_length=500, blank=True)
    sample_quality_extra_budjet = models.BooleanField(blank=True)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'steps'.lower()


class Questions(models.Model):
    question_id = models.CharField(max_length=37, primary_key=True)
    sr_id = models.CharField(max_length=37) # FK table service_requests
    question = models.TextField(max_length=500, blank=True)
    answer = models.TextField(max_length=500, blank=True)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'questions'.lower()




class Administration(models.Model):
    uuid = models.CharField(max_length=37, primary_key=True, default=uuid4())
    labname = models.CharField(max_length=50)
    dmptitle = models.CharField(max_length=128, blank=True)
    datausername = models.CharField(max_length=50)
    email = models.CharField(max_length=128, blank=True)
    affiliation = models.CharField(max_length=128, blank=True)
    experimentabstract = models.TextField(max_length=500, blank=True)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'administration'.lower()

class lageSample(models.Model):
    widgets = {}

    uuid = models.CharField(max_length=37, primary_key=True, default=uuid4())
    datausername = models.CharField(max_length=50)
    sample_description = models.TextField(max_length=500)
    
    type_of_sample_choices = (
        ("DNA","DNA"),
        ("RNA","RNA"),
        ("pellet","pellet"),
        ("biopsy","biopsy"),
    )
    type_of_sample = models.CharField(blank=True)
    widgets["type_of_sample"] = MultiChoicheAndOtherWidget(choices=type_of_sample_choices)

    is_volume_in_uL = models.CharField(blank=True)
    widgets["is_volume_in_uL"] = BooleanIfWhat(yes_or_no=False)

    is_buffer_used = models.CharField(blank=True)
    widgets["is_buffer_used"] = BooleanIfWhat(yes_or_no=False)

    expected_date_of_delivery = models.DateField(blank=True)
    
    is_quality = models.CharField(blank=True)
    widgets["is_quality"] = BooleanIfWhat(yes_or_no=False)

    sample_back = models.BooleanField(blank=True)

    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'uploads/{0}/{1}/{2}'.format(instance.datausername, instance.uuid, filename)

    samplesheet_file = models.FileField(blank=True, upload_to=user_directory_path)

    additional_files = models.FileField(blank=True, upload_to=user_directory_path)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'lagesample'.lower()


class labDMP(models.Model):
    labname = models.CharField(max_length=128, primary_key=True)
    datausername = models.CharField(max_length=50)
    # 'A) Do you collect all the metadata produced by your instruments?',3)
    instrument_metadata_collection =  models.CharField(max_length=128,blank=True)

    # 'B) Do you collect additional metadata by an open source laboratory notebook?',3)
    additional_enotebook_open_collection = models.CharField(max_length=128,blank=True)
    # 'C) Do you use a well defined standard to name your samples?',3)
    sample_standard = models.CharField(max_length=128,blank=True)
    # 'D) Do you use a well defined metadata schema and format?',3)
    metadata_schema_defined = models.CharField(blank=True) # TODO: IF YES WICH ONE (do the widget)
    # 'III Publication phase',1)
    # 'All the answers below have to be understood in the PRP project context, that is the implementations required by the project are developing the scenario described below.')
    # '1. Data and metadata publication',2)
    # 'A) Will data and related metadata be published on an open and trusted repository with a d.o.i.?',3)
    open_trusted_repo_published_data = models.BooleanField(blank=True)
    # 'B) Will published processed data and related metadata be licensed?',3)
    open_data_licence = models.CharField(blank=True)

    # '2. Scientific publications',2)
    # 'A) Will any scientific publication arising from data and related metadata be published on an open access peer review journal or uploaded on an open access repository?',3)
    open_access_journal_publication = models.BooleanField(blank=True)

    # B) Will any scientific publication have a clear data provenance?',3)
    clear_data_provenance = models.BooleanField(blank=True)

    # 'C) Will any scientific output related to data such as presentation or posters be open access registered with a d.o.i.?',3)
    related_data_open = models.BooleanField(blank=True)

    # 'D) Will scientific publication or any other scientific document (presentation, poster, etc.) be licensed?',3)
    licence_scientific_documents = models.BooleanField(blank=True)

    # 'IV Data and Metadata storage and preservation',1)
    # '1. Storage',2)
    # 'A) Where will raw data  be stored ?',3)
    raw_data_storage_location = models.CharField(blank=True)

    # 'B) How long will raw data be preserved ?',3)
    raw_data_storage_time_retention = models.CharField(blank=True)


    # '2. Backups',2)
    # 'A) Which backup policy will be applied to published data or raw data related to published data?',3)
    backup_policy_published_data = models.CharField(blank=True)

    # 'B) Which backup policy will be applied to not published data or raw data not related to published data?',3)
    backup_policy_unplublished_data = models.CharField(blank=True)

    class Meta:
        db_table= 'labdmp'.lower()
    

