# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-10 06:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0038_evento_permalink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='approved',
        ),
        migrations.AddField(
            model_name='evento',
            name='highlighted',
            field=models.BooleanField(default=False),
        ),
    ]
