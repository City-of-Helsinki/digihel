from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, \
    PageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index


content_blocks = [
    ('heading', blocks.CharBlock(classname="full title")),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageChooserBlock()),
]


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True,
                                  related_name='+')
    link_document = models.ForeignKey('wagtaildocs.Document', null=True, blank=True,
                                      related_name='+')

    @property
    def url(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


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
