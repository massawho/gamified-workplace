# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-09 20:51
from __future__ import unicode_literals

import apps.tcc.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0009_auto_20161005_0302'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='photo',
            field=models.ImageField(null=True, upload_to=apps.tcc.models.images_path),
        ),
    ]
