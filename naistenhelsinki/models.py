# -*- coding: utf-8 -*-
from django.contrib.gis.forms.widgets import OSMWidget
from django.contrib.gis.geos.point import Point
from django.db import models
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from django.contrib.gis.db import models as geomodels

HELSINKI = Point(24.945831, 60.192059)


class PlaceMapPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]


class Place(Orderable, Page):
    description = RichTextField("kuvaus", blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    location = geomodels.PointField(
        "paikka",
        null=True,
        blank=True,
        default=HELSINKI,
    )

    search_fields = Page.search_fields + [
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('description', classname="full"),
        FieldPanel('location', classname="full", widget=OSMWidget())
    ]


class PlaceListPage(Page):

    subpage_types = ['naistenhelsinki.Place']

    def places(self):
        return Place.objects.live()
