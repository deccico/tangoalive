# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-05-15 23:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0045_grupo_permalink'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='evento',
            name='recurrent_definition',
        ),
        migrations.AddField(
            model_name='evento',
            name='finish_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='weekly_recurrent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='eventos.Week'),
        ),
    ]
