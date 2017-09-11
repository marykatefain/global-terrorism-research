# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-09 17:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gtr_site', '0025_remove_statement_solokeywords'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keywordincontext',
            old_name='keyword',
            new_name='main_keyword',
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='statement',
        ),
        migrations.RemoveField(
            model_name='keywordincontext',
            name='contexts',
        ),
        migrations.AddField(
            model_name='keywordincontext',
            name='context',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keyword_context', to='gtr_site.Keyword'),
        ),
    ]