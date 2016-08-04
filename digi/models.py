from django.utils.translation import ugettext_lazy as _
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailsearch import index
from blog.models import BlogPage, BlogCategory


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


class ThemeIndexPage(Page):
    subpage_types = ['ThemePage']


class ThemePage(Page):
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                              on_delete=models.SET_NULL, related_name='+')
    short_description = models.TextField()
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
    ], null=True, blank=True)
    blog_category = models.ForeignKey(BlogCategory, help_text='Corresponding blog category',
                                      null=True, blank=True, on_delete=models.SET_NULL)

    parent_page_types = ['ThemeIndexPage']
    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('short_description'),
        FieldPanel('blog_category'),
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


class ProjectPage(Page):
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
