# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 07:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0003_auto_20160915_0157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('created_at', models.DateField()),
                ('ended_at', models.DateField(blank=True, null=True)),
                ('members', models.ManyToManyField(to='tcc.Employee')),
            ],
        ),
    ]