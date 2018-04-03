# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeentry', '0004_estimate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='dt',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='entry',
            name='ot',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='entry',
            name='reg',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='hours',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='job',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=11),
        ),
    ]