from django.db import models
# This apps is reserved to create the models of our external database schema
# through django ORM
from uuid import uuid4

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
    datausername = models.CharField(max_length=50)
    email = models.CharField(max_length=128, blank=True)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'administration'.lower()

class lageSample(models.Model):
    uuid = models.CharField(max_length=37, primary_key=True, default=uuid4())
    datausername = models.CharField(max_length=50)
    sample_description = models.TextField(max_length=500)

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'lagesample'.lower()

class lameSample(models.Model):
    # orid = models.ForeignKey(Administration, on_delete=models.CASCADE, blank=True)
    uuid = models.CharField(max_length=37, primary_key=True, default=uuid4())
    datausername = models.CharField(max_length=50)
    technique_description = models.CharField(max_length=128)
    device = models.CharField(max_length=50)


    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'lamesample'.lower()

class ladeSample(models.Model):
    # orid = models.ForeignKey(Administration, on_delete=models.CASCADE, blank=True)
    uuid = models.CharField(max_length=37, primary_key=True, default=uuid4())
    datausername = models.CharField(max_length=50)
    datacenter = models.CharField(max_length=128)
    gpu = models.CharField(max_length=50)


    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'ladesample'.lower()