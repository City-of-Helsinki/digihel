# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-19 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digi', '0014_projectpage_phase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='themepage',
            name='twitter_hashtag',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]