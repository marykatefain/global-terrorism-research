# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-27 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtr_site', '0019_auto_20170727_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='full_text',
            field=models.URLField(blank=True, null=True),
        ),
    ]
