# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-23 06:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0019_evento_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]