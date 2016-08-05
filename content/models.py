from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index


content_blocks = [
    ('heading', blocks.CharBlock(classname="full title")),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageChooserBlock()),
]


class TwoColumnBlock(blocks.StructBlock):
    left_column = blocks.StreamBlock(content_blocks, icon='arrow-left',
                                     label=_('Left column content'))
    right_column = blocks.StreamBlock(content_blocks, icon='arrow-right',
                                      label=_('Right column content'))

    class Meta:
        icon = 'placeholder'
        label = _('Two columns')
        template = 'content/blocks/two_column.html'


class ContentPage(Page):
    body = StreamField(content_blocks + [
        ('two_columns', TwoColumnBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]
