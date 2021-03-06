# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-22 16:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import timeentry.models


class Migration(migrations.Migration):

    dependencies = [
        ('timeentry', '0019_auto_20180221_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClockIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeentry.Employee')),
            ],
        ),
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(blank=True, default=timeentry.models.today, null=True),
        ),
    ]
