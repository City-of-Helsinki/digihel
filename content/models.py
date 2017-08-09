from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index
from wagtail_svgmap.blocks import ImageMapBlock

from digihel.mixins import RelativeURLMixin

rich_text_blocks = [
    ('heading', blocks.CharBlock(classname="full title")),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageChooserBlock()),
    ('table', TableBlock()),
    ('image_map', ImageMapBlock()),
]


class TwoColumnBlock(blocks.StructBlock):
    left_column = blocks.StreamBlock(rich_text_blocks, icon='arrow-left',
                                     label=_('Left column content'))
    right_column = blocks.StreamBlock(rich_text_blocks, icon='arrow-right',
                                      label=_('Right column content'))

    class Meta:
        icon = 'placeholder'
        label = _('Two columns')
        template = 'content/blocks/two_column.html'


content_blocks = rich_text_blocks + [
    ('two_columns', TwoColumnBlock()),
    ('collapsible', blocks.RichTextBlock(
        icon="collapse-down",
        label=_('Collapsible paragraph'),
        template='content/blocks/collapsible.html',
    )),
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


class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class ContentPage(RelativeURLMixin, Page):
    body = StreamField(content_blocks)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]


class LinkedContentPage(RelativeURLMixin, Page):
    body = StreamField(content_blocks)

    content_panels = Page.content_panels + [
        InlinePanel('roles', label=_("Roles")),
        InlinePanel('links', label=_("Links")),
        StreamFieldPanel('body'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]


class LinkedContentPageRole(Orderable):
    page = ParentalKey(LinkedContentPage, related_name='roles')
    person = models.ForeignKey('people.Person', db_index=True, related_name='+')
    role = models.CharField(max_length=100, null=True, blank=True)

    panels = [
        FieldPanel('person'),
        FieldPanel('role'),
    ]

    def __str__(self):
        return "{} with role {} on {}".format(self.person, self.role, self.theme)


class LinkedContentPageLink(Orderable, RelatedLink):
    page = ParentalKey(LinkedContentPage, related_name='links')
