# Generated by Django 5.0.6 on 2024-07-17 07:30

import PRP_CDM_app.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PRP_CDM_app', '0005_alter_administration_uuid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lagesample',
            name='file_in',
        ),
        migrations.AddField(
            model_name='lagesample',
            name='additional_files',
            field=models.FileField(blank=True, upload_to=PRP_CDM_app.models.lageSample.user_directory_path),
        ),
        migrations.AddField(
            model_name='lagesample',
            name='samplesheet_file',
            field=models.FileField(blank=True, upload_to=PRP_CDM_app.models.lageSample.user_directory_path),
        ),
        migrations.AlterField(
            model_name='administration',
            name='uuid',
            field=models.CharField(default=uuid.UUID('2bde91e1-d6a8-43d0-8e5f-70f5facfad12'), max_length=37, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customappmodel',
            name='datavarchar',
            field=models.CharField(default=uuid.UUID('2d4c55f3-e1e7-4f1c-99ac-46cb44d08b37'), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lagesample',
            name='uuid',
            field=models.CharField(default=uuid.UUID('6cc1220f-6424-430b-bf24-e5c29886ca39'), max_length=37, primary_key=True, serialize=False),
        ),
    ]
