# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-19 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtr_site', '0009_auto_20170717_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='produced_by',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
