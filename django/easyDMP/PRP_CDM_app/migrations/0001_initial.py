# Generated by Django 5.0.6 on 2024-07-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomAppModel',
            fields=[
                ('datavarchar', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('datausername', models.CharField(blank=True, max_length=255)),
                ('dataint', models.IntegerField()),
            ],
            options={
                'db_table': 'customappmodel',
            },
        ),
    ]
