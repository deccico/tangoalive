# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-05-15 23:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0046_auto_20170515_2000'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Week',
            new_name='Day',
        ),
        migrations.RenameField(
            model_name='evento',
            old_name='weekly_recurrent',
            new_name='weekly_recurrence',
        ),
    ]
