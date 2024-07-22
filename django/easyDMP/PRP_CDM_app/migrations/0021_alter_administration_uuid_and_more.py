# Generated by Django 5.0.6 on 2024-07-18 15:28

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PRP_CDM_app', '0020_alter_administration_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administration',
            name='uuid',
            field=models.CharField(default=uuid.UUID('01247f44-b644-4226-95ff-f81e4966bfa9'), max_length=37, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customappmodel',
            name='datavarchar',
            field=models.CharField(default=uuid.UUID('420721db-8ea9-43a8-a6f2-047bb06da4d2'), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lagesample',
            name='uuid',
            field=models.CharField(default=uuid.UUID('cafa62c5-c163-4015-8b13-8a13966a9ca4'), max_length=37, primary_key=True, serialize=False),
        ),
    ]