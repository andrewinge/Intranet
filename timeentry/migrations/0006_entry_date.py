# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeentry', '0005_auto_20170329_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
