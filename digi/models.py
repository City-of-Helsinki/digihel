from blog.models import BlogCategory, BlogIndexPage, BlogPage
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

from content.models import RelatedLink
from digihel.mixins import RelativeURLMixin
from events.models import EventsIndexPage

from news.news import get_news_cached

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
    slug = models.CharField(max_length=100, default='')
    value = models.IntegerField()  # no history data for now
    order = models.IntegerField(null=True, blank=True)
    front_page = models.BooleanField(default=False)
    illustration_filename = models.CharField(max_length=100, default='images/hki-tietoaineisto.svg')
    source_description = models.CharField(max_length=200, default='')
    source_url = models.CharField(max_length=100, default='http://dev.hel.fi/apis')

    sort_order_field = 'order'

    class Meta:
        verbose_name = _('Indicator')
        verbose_name_plural = _('Indicators')
        ordering = ['order']

    def __str__(self):
        return self.description


class Banner(models.Model):
    header = models.CharField(_('Header'), max_length=100, default='')
    text = models.CharField(_('Text'), max_length=255)
    link_text = models.CharField(_('Link text'), max_length=50)
    link_url = models.CharField(_('Link URL'), max_length=100, default='')
    icon_file = models.FileField(_('Icon file'))
    icon_alt_text = models.CharField(_('Icon alt text'), max_length=100, default='')
    order = models.IntegerField(_('Order'), null=True, blank=True)

    sort_order_field = 'order'

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        ordering = ['order']

    def __str__(self):
        return self.header


class Phase():
    NONE = ''
    DISCOVERY = 'DI'
    ALPHA = 'AL'
    BETA = 'BE'
    LIVE = 'LI'
    RETIREMENT = 'RE'

    PHASE_CHOICES = (
        (NONE, 'No phase'),
        (DISCOVERY, 'Selvitys'),
        (ALPHA, 'Alfa'),
        (BETA, 'Beta'),
        (LIVE, 'Tuotanto'),
        (RETIREMENT, 'Poisto'),
    )

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
    guides_and_support_header = models.CharField(_('Guides and support header'), max_length=100, default="", null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('guides_and_support_header')
    ]

    subpage_types = ['ThemePage']

    @property
    def front_page_themes(self):
        return ThemePage.objects.live().filter(promote_on_front_page=True)

    @property
    def guides_and_support_themes(self):
        return ThemePage.objects.live().exclude(promote_on_front_page=True)


class GuideFrontPage(RelativeURLMixin, Page):

    @property
    def blog_posts(self):
        posts = BlogPage.objects.descendant_of(self).live().order_by('-date')
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
    twitter_hashtag = models.CharField(max_length=255, default="", null=True, blank=True)
    promote_on_front_page = models.BooleanField(default=False, help_text='Show summary on front page')

    parent_page_types = ['ThemeIndexPage']
    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('type'),
        FieldPanel('short_description'),
        FieldPanel('blog_category'),
        FieldPanel('twitter_hashtag'),
        InlinePanel('roles', label=_("Roles")),
        InlinePanel('links', label=_("Links")),
        StreamFieldPanel('body'),
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel('promote_on_front_page'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('body'),
    ]
    subpage_types = ['ProjectPage']

    @property
    def projects(self):
        return self.get_children().exact_type(ProjectPage).live().specific()

    def get_context(self, request, **kwargs):
        context = super(ThemePage, self).get_context(request, **kwargs)
        context['projects_title'] = _('Kokonaisuuteen kuuluu:')
        context['projects'] = self.projects
        return context


class ThemeRole(Orderable):
    theme = ParentalKey(ThemePage, related_name='roles')
    person = models.ForeignKey('people.Person', db_index=True, related_name='theme_roles', on_delete=models.CASCADE)
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
    phase = models.CharField(max_length=2,choices=Phase.PHASE_CHOICES,default=Phase.NONE,null=True, blank=True)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
    ], null=True, blank=True)

    twitter_hashtag = models.CharField(max_length=255, default="", null=True, blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('short_description'),
        FieldPanel('phase'),
        FieldPanel('twitter_hashtag'),
        InlinePanel('roles', label=_("Roles")),
        InlinePanel('links', label=_("Links")),
        StreamFieldPanel('body'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('body'),
    ]
    parent_page_types = ['ThemePage']

    def get_context(self, request, **kwargs):
        context = super(ProjectPage, self).get_context(request, **kwargs)
        context['projects_title'] = _('Lisää aiheesta: ') + self.get_parent().title
        context['projects'] = self.get_parent().get_children().exclude(id=self.id)\
            .exact_type(ProjectPage).live().specific()
        return context


class ProjectRole(Orderable):
    project = ParentalKey(ProjectPage, db_index=True, related_name='roles')
    person = models.ForeignKey('people.Person', db_index=True, related_name='project_roles', on_delete=models.CASCADE)
    role = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "{} with role {} on {}".format(self.person, self.role, self.theme)


class ProjectLink(Orderable, RelatedLink):
    theme = ParentalKey('digi.ProjectPage', related_name='links')


class FrontPage(RelativeURLMixin, Page):
    hero_background = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                              on_delete=models.SET_NULL, related_name='+')
    themes_header = models.CharField(_('Themes header'), max_length=100, default="", null=True, blank=True)
    projects_header = models.CharField(_('Projects header'), max_length=100, default="", null=True, blank=True)
    banners_header = models.CharField(_('Banner header'), max_length=100, default="", null=True, blank=True)
    news_header = models.CharField(_('News header'), max_length=100, default="", null=True, blank=True)

    news_index_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    hero = StreamField([
        ('paragraph', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('themes_header'),
                FieldPanel('projects_header'),
                FieldPanel('banners_header'),
                FieldPanel('news_header'),
            ],
            heading=_('Collection of Main Headers'),
            classname='collapsible collapsed'
        ),
        ImageChooserPanel('hero_background'),
        StreamFieldPanel('hero'),
        PageChooserPanel('news_index_page', 'news.NewsIndexPage'),
    ]

    @property
    def indicators(self):
        return Indicator.objects.filter(front_page=True)

    @property
    def banners(self):
        return Banner.objects.all()

    @property
    def themes(self):
        return ThemePage.objects.all()

    @property
    def projects(self):
        return ProjectPage.objects.all().live().in_menu()

    @property
    def news_index(self):
        if self.news_index_page:
            return self.news_index_page
        return self

    @property
    def news_feeds(self):
        return get_news_cached(self.news_index.url)

    @property
    def event_index(self):
        return EventsIndexPage.objects.live().first()

    @property
    def footer_link_sections(self):
        return FooterLinkSection.objects.order_by('sort_order')
