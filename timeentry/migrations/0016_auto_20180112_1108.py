# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-12 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeentry', '0015_auto_20171009_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='foreman',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employee',
            name='pto',
            field=models.IntegerField(default=15),
        ),
    ]
