# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 18:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gtr_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context_word', models.CharField(max_length=200)),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtr_site.Keyword')),
            ],
        ),
    ]
