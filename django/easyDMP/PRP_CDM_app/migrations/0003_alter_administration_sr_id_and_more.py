# Generated by Django 5.1 on 2024-09-10 10:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PRP_CDM_app', '0002_administration_instruments_instrumentxtechnique_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administration',
            name='sr_id',
            field=models.CharField(default=uuid.UUID('f768b320-19fe-4f87-994c-3684fdbf3aec'), max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='instruments',
            name='instrument_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='instrumentxtechnique',
            name='x_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='laboratories',
            name='lab_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='labxinstrument',
            name='x_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='proposals',
            name='proposal_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='questions',
            name='question_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='samples',
            name='sample_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='servicerequests',
            name='sr_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='steps',
            name='step_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='techniques',
            name='technique_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
