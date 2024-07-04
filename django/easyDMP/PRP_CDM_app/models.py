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

class Laboratories(models.Model):
    id_name = models.CharField(max_length=50, primary_key=True)
    full_name = models.CharField(max_length=255)

    class Meta:
        db_table= 'laboratories'.lower()