from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from helsinkioppii.blocks.case_lift import CaseLiftBlock


class HelsinkiOppiiIndexPage(Page):
    template = 'helsinkioppii/index.html'

    hero_title = models.CharField(
        verbose_name=_('lift title'),
        max_length=256,
        blank=True,
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('hero image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    case_lifts = StreamField([
        ('case', CaseLiftBlock()),
    ], blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        StreamFieldPanel('case_lifts'),
        FieldPanel('hero_title'),
    ]
