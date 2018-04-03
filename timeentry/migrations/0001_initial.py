# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg', models.DecimalField(decimal_places=2, max_digits=3)),
                ('ot', models.DecimalField(decimal_places=2, max_digits=3)),
                ('dt', models.DecimalField(decimal_places=2, max_digits=3)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeentry.Category')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeentry.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('customer', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('v1', models.BooleanField(default=False)),
                ('v2', models.BooleanField(default=False)),
                ('v3', models.BooleanField(default=False)),
                ('f1', models.BooleanField(default=False)),
                ('f2', models.BooleanField(default=False)),
                ('f3', models.BooleanField(default=False)),
                ('h1', models.BooleanField(default=False)),
                ('h2', models.BooleanField(default=False)),
                ('h3', models.BooleanField(default=False)),
                ('i1', models.BooleanField(default=False)),
                ('i2', models.BooleanField(default=False)),
                ('i3', models.BooleanField(default=False)),
                ('s1', models.BooleanField(default=False)),
                ('s2', models.BooleanField(default=False)),
                ('s3', models.BooleanField(default=False)),
                ('podate', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('description', models.CharField(blank=True, max_length=10, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeentry.Group')),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeentry.Job'),
        ),
        migrations.AddField(
            model_name='entry',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='timeentry.Task'),
        ),
    ]
