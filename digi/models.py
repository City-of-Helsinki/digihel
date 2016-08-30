from django.utils.translation import ugettext_lazy as _
from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, \
    InlinePanel, MultiFieldPanel
from wagtail.wagtailsearch import index
from blog.models import BlogPage, BlogCategory
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from content.models import LinkFields


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
        InlinePanel('links', label="Links"),
    ]

    def __str__(self):
        return self.title


class FooterLink(Orderable, RelatedLink):
    section = ParentalKey('digi.FooterLinkSection', related_name='links')


class ThemeIndexPage(Page):
    subpage_types = ['ThemePage']


class ThemePage(Page):
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
        InlinePanel('roles', label="Roles"),
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
    person = models.ForeignKey('people.Person', db_index=True)
    role = models.CharField(max_length=100, null=True, blank=True)

    panels = [
        FieldPanel('person'),
        FieldPanel('role'),
    ]

    def __str__(self):
        return "{} with role {} on {}".format(self.person, self.role, self.theme)


class ProjectPage(Page):
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
        StreamFieldPanel('body'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('body'),
    ]
    parent_page_types = ['ThemePage']


class ProjectRole(Orderable):
    project = ParentalKey(ProjectPage, db_index=True)
    person = models.ForeignKey('people.Person', db_index=True)
    role = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "{} with role {} on {}".format(self.person, self.role, self.theme)


class FrontPage(Page):
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
        return BlogPage.objects.all()

    @property
    def footer_link_sections(self):
        return FooterLinkSection.objects.order_by('sort_order')
