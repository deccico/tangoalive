# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-23 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0016_auto_20160722_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musico',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='musicos_pics/%Y_%m/%d/%H_%M_%S//'),
        ),
    ]