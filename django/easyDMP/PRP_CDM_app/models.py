from django.db import models

# This apps is reserved to create the models of our external database schema
# through django ORM

class CustomAppModel(models.Model):
    # If you don't put an explicit primary_key an autoincrement id will be used instead
    # TODO: foreign keys
    datavarchar = models.CharField(max_length=255, primary_key=True)
    datausername = models.CharField(max_length=255, blank=True)
    dataint = models.IntegerField()

    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'customappmodel'.lower()

class Administration(models.Model):
    orid = models.CharField(max_length=50, primary_key=True)
    email = models.CharField(max_length=128, blank=True)
    datausername = models.CharField(max_length=50)


    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'administration'.lower()

class lageSample(models.Model):
    # orid = models.ForeignKey(Administration, on_delete=models.CASCADE, blank=True)
    sample_description = models.CharField(max_length=500)
    datausername = models.CharField(max_length=50)


    # give the name of the table, lowercase for postgres (I've put a "lower() to remember")
    class Meta:
        db_table= 'lagesample'.lower()
