# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-06 20:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timeentry', '0009_auto_20170412_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='dt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='entry',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='timeentry.Job'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='ot',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='entry',
            name='reg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
