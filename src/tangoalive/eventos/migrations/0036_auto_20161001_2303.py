# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-02 02:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0035_evento_precio_evento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evento',
            old_name='precio_evento',
            new_name='precio_entrada',
        ),
    ]
