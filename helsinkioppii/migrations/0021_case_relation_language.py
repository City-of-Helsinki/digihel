# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-16 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helsinkioppii', '0020_page_group_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='student_count',
        ),
        migrations.AddField(
            model_name='casetheme',
            name='language_code',
            field=models.CharField(choices=[('fi', 'Suomi'), ('sv', 'Svenska'), ('en', 'English')], default='fi', max_length=10, verbose_name='language code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolgrade',
            name='language_code',
            field=models.CharField(choices=[('fi', 'Suomi'), ('sv', 'Svenska'), ('en', 'English')], default='fi', max_length=10, verbose_name='language code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolsubject',
            name='language_code',
            field=models.CharField(choices=[('fi', 'Suomi'), ('sv', 'Svenska'), ('en', 'English')], default='fi', max_length=10, verbose_name='language code'),
            preserve_default=False,
        ),
    ]
