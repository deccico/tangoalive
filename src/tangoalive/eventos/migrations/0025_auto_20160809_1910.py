# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-09 22:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0024_auto_20160806_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='grupo',
        ),
        migrations.AddField(
            model_name='evento',
            name='grupo',
            field=models.ManyToManyField(blank=True, null=True, to='eventos.Grupo'),
        ),
    ]