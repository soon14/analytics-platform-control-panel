# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_panel_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
