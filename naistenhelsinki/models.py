
from django.db import models
from django.conf import settings
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class PlacePage(Orderable, Page):
    name = models.CharField("aineiston nimi", max_length=300, blank=False, null=False, unique=True)
    description = RichTextField("kuvaus", blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    search_fields = Page.search_fields + (
        index.SearchField('name'),
        index.SearchField('description'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        ImageChooserPanel('image'),
        FieldPanel('description', classname="full")
    ]


class PlacesIndexPage(Page):

    subpage_types = ['naistenhelsinki.PlacePage']

    def places(self):
        return PlacePage.objects.live()
