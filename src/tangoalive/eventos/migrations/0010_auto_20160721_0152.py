# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-21 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0009_auto_20160721_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='eventos/static/eventos/eventos_pics/%Y_%m_%d_%H_%M_%S/'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='eventos/static/eventos/eventos_pics/%Y_%m_%d_%H_%M_%S/'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to='eventos/static/eventos/eventos_pics/%Y_%m_%d_%H_%M_%S/'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='image_4',
            field=models.ImageField(blank=True, null=True, upload_to='eventos/static/eventos/eventos_pics/%Y_%m_%d_%H_%M_%S/'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='image_5',
            field=models.ImageField(blank=True, null=True, upload_to='eventos/static/eventos/eventos_pics/%Y_%m_%d_%H_%M_%S/'),
        ),
    ]