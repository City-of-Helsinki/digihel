from blog.models import BlogCategory, BlogPage
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index

from content.models import RelatedLink
from digihel.mixins import RelativeURLMixin
from events.models import EventsIndexPage

rich_text_blocks = [
    ('heading', blocks.CharBlock(classname="full title")),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageChooserBlock()),
]

guide_blocks = rich_text_blocks + [
    ('raw_content', blocks.RawHTMLBlock()),
]

class Indicator(models.Model):
    description = models.CharField(max_length=200)
    value = models.IntegerField()  # no history data for now
    order = models.IntegerField(null=True, blank=True)
    front_page = models.BooleanField(default=False)

    sort_order_field = 'order'

    class Meta:
        verbose_name = _('Indicator')
        verbose_name_plural = _('Indicators')
        ordering = ['order']

    def __str__(self):
        return self.description


class FooterLinkSection(ClusterableModel):
    title = models.CharField(max_length=100, null=True, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('sort_order'),
        InlinePanel('links', label=_("Links")),
    ]

    def __str__(self):
        return self.title


class FooterLink(Orderable, RelatedLink):
    section = ParentalKey('digi.FooterLinkSection', related_name='links')




class ThemeIndexPage(RelativeURLMixin, Page):
    subpage_types = ['ThemePage']

    @property
    def themes(self):
        return ThemePage.objects.all()


class GuideFrontPage(RelativeURLMixin, Page):

    @property
    def blog_posts(self):
        posts = BlogPage.objects.all().live().filter(tags__name='digipalveluopas').order_by('-date')
        return posts

class GuideContentPage(RelativeURLMixin, Page):
    body = StreamField(guide_blocks)
    sidebar = StreamField(guide_blocks)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        StreamFieldPanel('sidebar')
    ]
    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

class ThemePage(RelativeURLMixin, Page):
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                              on_delete=models.SET_NULL, related_name='+')
    type = models.CharField(max_length=10, default="Teema")
    short_description = models.TextField()
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
    ], null=True, blank=True)
    blog_category = models.ForeignKey(BlogCategory, help_text='Corresponding blog category',
                                      null=True, blank=True, on_delete=models.SET_NULL)

    parent_page_types = ['ThemeIndexPage']
    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('type'),
        FieldPanel('short_description'),
        FieldPanel('blog_category'),
        InlinePanel('roles', label=_("Roles")),
        InlinePanel('links', label=_("Links")),
        StreamFieldPanel('body'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('body'),
    ]
    subpage_types = ['ProjectPage']

    @property
    def projects(self):
        return self.get_children().exact_type(ProjectPage).live().specific()


class ThemeRole(Orderable):
    theme = ParentalKey(ThemePage, related_name='roles')
    person = models.ForeignKey('people.Person', db_index=True, related_name='theme_roles')
    role = models.CharField(max_length=100, null=True, blank=True)

    panels = [
        FieldPanel('person'),
        FieldPanel('role'),
    ]

    def __str__(self):
        return "{} with role {} on {}".format(self.person, self.role, self.theme)


class ThemeLink(Orderable, RelatedLink):
    theme = ParentalKey('digi.ThemePage', related_name='links')


class ProjectPage(RelativeURLMixin, Page):
    type = _('Project')
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                              on_delete=models.SET_NULL, related_name='+')
    short_description = models.TextField(null=True, blank=True)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('short_description'),
        InlinePanel('roles', label=_("Roles")),
        InlinePanel('links', label=_("Links")),
        StreamFieldPanel('body'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('body'),
    ]
    parent_page_types = ['ThemePage']


class ProjectRole(Orderable):
    project = ParentalKey(ProjectPage, db_index=True, related_name='roles')
    person = models.ForeignKey('people.Person', db_index=True, related_name='project_roles')
    role = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "{} with role {} on {}".format(self.person, self.role, self.theme)


class ProjectLink(Orderable, RelatedLink):
    theme = ParentalKey('digi.ProjectPage', related_name='links')


class FrontPage(RelativeURLMixin, Page):
    hero = StreamField([
        ('paragraph', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('hero'),
    ]

    @property
    def indicators(self):
        return Indicator.objects.filter(front_page=True)

    @property
    def themes(self):
        return ThemePage.objects.all()

    @property
    def blog_posts(self):
        posts = BlogPage.objects.all().live().order_by('-date')
        return posts

    @property
    def event_index(self):
        return EventsIndexPage.objects.live().first()

    @property
    def footer_link_sections(self):
        return FooterLinkSection.objects.order_by('sort_order')
