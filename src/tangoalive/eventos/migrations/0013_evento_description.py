# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-22 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0012_auto_20160722_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
