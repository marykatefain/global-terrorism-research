# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtr_site', '0004_auto_20170315_1945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='context',
            name='keyword',
        ),
        migrations.AddField(
            model_name='context',
            name='keyword',
            field=models.ManyToManyField(to='gtr_site.Keyword'),
        ),
        migrations.RemoveField(
            model_name='context',
            name='statement',
        ),
        migrations.AddField(
            model_name='context',
            name='statement',
            field=models.ManyToManyField(to='gtr_site.Statement'),
        ),
    ]
