# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-08 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('benteler', '0004_auto_20170108_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='parent_place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='benteler.Place', verbose_name='ParentPlace'),
        ),
        migrations.AlterField(
            model_name='place',
            name='parts',
            field=models.ManyToManyField(blank=True, to='benteler.Part', verbose_name='Parts'),
        ),
    ]