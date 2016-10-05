# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='description',
            field=models.CharField(blank=True, help_text='A brief description for this questionnaire', max_length=255, null=True),
        ),
    ]