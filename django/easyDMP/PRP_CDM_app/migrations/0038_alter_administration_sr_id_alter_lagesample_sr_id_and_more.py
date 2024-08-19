# Generated by Django 5.1 on 2024-08-19 10:25

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PRP_CDM_app', '0037_alter_administration_sr_id_alter_lagesample_sr_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administration',
            name='sr_id',
            field=models.CharField(default=uuid.UUID('67a09454-271c-423b-8064-1709d3ea0fa6'), max_length=37, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lagesample',
            name='sr_id',
            field=models.CharField(default=uuid.UUID('a8659c57-8874-42a3-b7c3-eb38e3c67e5b'), max_length=37, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='proposals',
            name='proposal_feasibility',
            field=models.CharField(blank=True, choices=[('feasible', 'feasible'), ('not feasible', 'not feasible'), ('feasible with reservations', 'feasible with reservations')]),
        ),
    ]
