# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-21 05:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0010_auto_20160721_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
