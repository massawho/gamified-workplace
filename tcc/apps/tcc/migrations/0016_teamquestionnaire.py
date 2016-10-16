# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-16 03:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_questionnaire_description'),
        ('tcc', '0015_auto_20161011_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamQuestionnaire',
            fields=[
                ('questionnaire', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='questionnaire.Questionnaire')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tcc.Team')),
            ],
        ),
    ]
