# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-14 20:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timeentry', '0017_auto_20180207_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeptCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeentry.Department')),
            ],
        ),
    ]
