# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 03:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tcc', '0006_employee_hiring_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tcc.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='A short name to describe the goal', max_length=40)),
                ('money', models.PositiveIntegerField(default=0, help_text='Diamonds received when employee finishes this goal', verbose_name='Diamonds')),
                ('level', models.PositiveIntegerField(choices=[(4, 'Platinum'), (3, 'Gold'), (2, 'Silver'), (1, 'Bronze')], default=1, help_text='The level of importance of this goal')),
                ('is_active', models.BooleanField(default=True)),
                ('products', models.ManyToManyField(blank=True, to='tcc.Product')),
            ],
        ),
        migrations.AddField(
            model_name='badge',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tcc.Goal'),
        ),
        migrations.AddField(
            model_name='employee',
            name='badges',
            field=models.ManyToManyField(through='tcc.Badge', to='tcc.Goal'),
        ),
    ]
