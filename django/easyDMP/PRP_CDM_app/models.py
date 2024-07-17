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




class CustomAppModel(models.Model):
    # If you don't put an explicit primary_key an autoincrement id will be used instead
    # TODO: foreign keys
    datavarchar = models.CharField(max_length=255, primary_key=True, default=uuid4())
    datausername = models.CharField(max_length=255, blank=True)
    dataint = models.IntegerField()

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'customappmodel'.lower()

class Administration(models.Model):
    uuid = models.CharField(max_length=37, primary_key=True, default=uuid4())
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

    is_volume_in_uL_choices = (
        ("Yes","Yes"),
    )
    is_volume_in_uL = models.CharField(blank=True)
    widgets["is_volume_in_uL"] = MultiChoicheAndOtherWidget(choices=is_volume_in_uL_choices)

    is_buffer_used_choices = (
        ("Yes","Yes"),
    )
    is_buffer_used = models.CharField(blank=True)
    widgets["is_buffer_used"] = MultiChoicheAndOtherWidget(choices=is_buffer_used_choices)

    expected_date_of_delivery = models.DateField(blank=True)

    is_quality_choices = (
        ("Yes","Yes"),
    )
    
    is_quality = models.CharField(blank=True)
    widgets["is_quality"] = MultiChoicheAndOtherWidget(choices=is_quality_choices)

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
    labname = models.CharField(max_length=50, primary_key=True)
    datausername = models.CharField(max_length=50)
    datageneric = models.CharField(max_length=128)
    # 'A) Do you collect all the metadata produced by your instruments?',3)
    instrument_metadata_collection =  models.CharField()

    # 'B) Do you collect additional metadata by an open source laboratory notebook?',3)
    additional_enotebook_open_collection = models.CharField()
    # 'C) Do you use a well defined standard to name your samples?',3)
    sample_standard = models.CharField()
    # 'D) Do you use a well defined metadata schema and format?',3)
    metadata_schema_defined = models.CharField() # TODO: IF YES WICH ONE (do the widget)
    # 'III Publication phase',1)
    # 'All the answers below have to be understood in the PRP project context, that is the implementations required by the project are developing the scenario described below.')
    # '1. Data and metadata publication',2)
    # 'A) Will data and related metadata be published on an open and trusted repository with a d.o.i.?',3)
    open_trusted_repo_published_data = models.CharField()
    # 'B) Will published processed data and related metadata be licensed?',3)
    open_data_licence = models.CharField()

    # '2. Scientific publications',2)
    # 'A) Will any scientific publication arising from data and related metadata be published on an open access peer review journal or uploaded on an open access repository?',3)
    open_access_journal_publication = models.CharField()

    # B) Will any scientific publication have a clear data provenance?',3)
    clear_data_provenance = models.CharField()

    # 'C) Will any scientific output related to data such as presentation or posters be open access registered with a d.o.i.?',3)
    related_data_open = models.CharField()

    # 'D) Will scientific publication or any other scientific document (presentation, poster, etc.) be licensed?',3)
    licence_scientific_documents = models.CharField()

    # 'IV Data and Metadata storage and preservation',1)
    # '1. Storage',2)
    # 'A) Where will raw data  be stored ?',3)
    raw_data_storage_location = models.CharField()

    # 'B) How long will raw data be preserved ?',3)
    raw_data_storage_time_retention = models.CharField()


    # '2. Backups',2)
    # 'A) Which backup policy will be applied to published data or raw data related to published data?',3)
    backup_policy_published_data = models.CharField()

    # 'B) Which backup policy will be applied to not published data or raw data not related to published data?',3)
    backup_policy_unplublished_data = models.CharField()

    class Meta:
        db_table= 'labdmp'.lower()
    

