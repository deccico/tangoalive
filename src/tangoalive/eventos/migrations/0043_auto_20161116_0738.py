# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-16 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0042_auto_20161113_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventoentrada',
            name='evento',
        ),
        migrations.AddField(
            model_name='evento',
            name='tipo_entradas',
            field=models.ManyToManyField(blank=True, to='eventos.EventoEntrada'),
        ),
    ]