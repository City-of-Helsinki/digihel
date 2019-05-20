# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-13 16:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtail_svgmap.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
        ('wagtaildocs', '0007_merge'),
        ('people', '0003_auto_20160913_1914'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkedContentPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image_map', wagtail.core.blocks.StructBlock((('map', wagtail_svgmap.blocks._ImageMapChoiceBlock(label='Image map', required=True)), ('css_class', wagtail.core.blocks.CharBlock(label='CSS class', required=False))))), ('two_columns', wagtail.core.blocks.StructBlock((('left_column', wagtail.core.blocks.StreamBlock((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image_map', wagtail.core.blocks.StructBlock((('map', wagtail_svgmap.blocks._ImageMapChoiceBlock(label='Image map', required=True)), ('css_class', wagtail.core.blocks.CharBlock(label='CSS class', required=False)))))), icon='arrow-left', label='Left column content')), ('right_column', wagtail.core.blocks.StreamBlock((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image_map', wagtail.core.blocks.StructBlock((('map', wagtail_svgmap.blocks._ImageMapChoiceBlock(label='Image map', required=True)), ('css_class', wagtail.core.blocks.CharBlock(label='CSS class', required=False)))))), icon='arrow-right', label='Right column content')))))))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='LinkedContentPageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.Document')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='content.LinkedContentPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LinkedContentPageRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('role', models.CharField(blank=True, max_length=100, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='content.LinkedContentPage')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='people.Person')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='contentpage',
            name='body',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image_map', wagtail.core.blocks.StructBlock((('map', wagtail_svgmap.blocks._ImageMapChoiceBlock(label='Image map', required=True)), ('css_class', wagtail.core.blocks.CharBlock(label='CSS class', required=False))))), ('two_columns', wagtail.core.blocks.StructBlock((('left_column', wagtail.core.blocks.StreamBlock((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image_map', wagtail.core.blocks.StructBlock((('map', wagtail_svgmap.blocks._ImageMapChoiceBlock(label='Image map', required=True)), ('css_class', wagtail.core.blocks.CharBlock(label='CSS class', required=False)))))), icon='arrow-left', label='Left column content')), ('right_column', wagtail.core.blocks.StreamBlock((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image_map', wagtail.core.blocks.StructBlock((('map', wagtail_svgmap.blocks._ImageMapChoiceBlock(label='Image map', required=True)), ('css_class', wagtail.core.blocks.CharBlock(label='CSS class', required=False)))))), icon='arrow-right', label='Right column content'))))))),
        ),
    ]
