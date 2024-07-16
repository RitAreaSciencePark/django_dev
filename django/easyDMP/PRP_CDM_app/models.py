from django.db import models
# This apps is reserved to create the models of our external database schema
# through django ORM
from django import forms
from uuid import uuid4
from .fields import MultiChoicheAndOtherWidget

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

    file_in = models.FileField(blank=True, upload_to="uploads/")

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'lagesample'.lower()
