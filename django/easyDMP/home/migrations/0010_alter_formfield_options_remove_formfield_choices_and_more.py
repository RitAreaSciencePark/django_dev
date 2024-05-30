# Generated by Django 5.0.6 on 2024-05-30 11:26

import django.core.serializers.json
import django.db.models.deletion
import wagtail.contrib.forms.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_formpage_formfield'),
        ('wagtailcore', '0093_uploadedfile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formfield',
            options={},
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='choices',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='clean_name',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='default_value',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='field_type',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='help_text',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='id',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='label',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='required',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='sort_order',
        ),
        migrations.AddField(
            model_name='formfield',
            name='from_address',
            field=models.EmailField(blank=True, max_length=255, verbose_name='from address'),
        ),
        migrations.AddField(
            model_name='formfield',
            name='page_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='formfield',
            name='subject',
            field=models.CharField(blank=True, max_length=255, verbose_name='subject'),
        ),
        migrations.AddField(
            model_name='formfield',
            name='to_address',
            field=models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, validators=[wagtail.contrib.forms.models.validate_to_address], verbose_name='to address'),
        ),
        migrations.CreateModel(
            name='CustomFormSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_data', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('submit_time', models.DateTimeField(auto_now_add=True, verbose_name='submit time')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.page')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'form submission',
                'verbose_name_plural': 'form submissions',
                'abstract': False,
            },
        ),
    ]
