# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-06 15:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gtr_site', '0029_statement_fulltext'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statement',
            old_name='fulltext',
            new_name='summary',
        ),
    ]
