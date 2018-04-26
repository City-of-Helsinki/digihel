# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-10 07:42
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('helsinkioppii', '0009_change_type_to_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helsinkioppiiindexpage',
            name='banner_lifts',
            field=wagtail.wagtailcore.fields.StreamField((('banner', wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('title', wagtail.wagtailcore.blocks.CharBlock(max_length=120)), ('abstract', wagtail.wagtailcore.blocks.TextBlock(max_length=225)), ('page_link', wagtail.wagtailcore.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Overrides page link if set.', required=False))))),), blank=True),
        ),
        migrations.AlterField(
            model_name='trainingindexpage',
            name='banner_lifts',
            field=wagtail.wagtailcore.fields.StreamField((('banner', wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('title', wagtail.wagtailcore.blocks.CharBlock(max_length=120)), ('abstract', wagtail.wagtailcore.blocks.TextBlock(max_length=225)), ('page_link', wagtail.wagtailcore.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Overrides page link if set.', required=False))))),), blank=True),
        ),
    ]
