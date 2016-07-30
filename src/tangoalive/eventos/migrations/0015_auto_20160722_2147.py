# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-23 00:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0014_auto_20160722_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='grupos_pics/%Y_%m/%d/%H_%M_%S//')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='grupos_pics/%Y_%m/%d/%H_%M_%S//')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='grupos_pics/%Y_%m/%d/%H_%M_%S//')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='grupos_pics/%Y_%m/%d/%H_%M_%S//')),
                ('image_5', models.ImageField(blank=True, null=True, upload_to='grupos_pics/%Y_%m/%d/%H_%M_%S//')),
                ('video_youtube', models.URLField(blank=True, null=True)),
                ('soundcloud', models.URLField(blank=True, null=True)),
                ('spotify', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('band_camp', models.URLField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='musico',
            name='grupos',
        ),
        migrations.DeleteModel(
            name='Grupos',
        ),
        migrations.AddField(
            model_name='grupo',
            name='grupos',
            field=models.ManyToManyField(blank=True, null=True, to='eventos.Musico'),
        ),
    ]