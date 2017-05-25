from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index

from content.models import content_blocks
from digihel.mixins import RelativeURLMixin
from search.fields import tag_search_field


class BaseModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    short_description = models.TextField(verbose_name=_('Short description'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class UserRole(BaseModel):
    class Meta:
        verbose_name = _('User role')
        verbose_name_plural = _('User roles')


class DevelopmentMethod(BaseModel):
    class Meta:
        verbose_name = _('Development method')
        verbose_name_plural = _('Development methods')


class DevelopmentPhase(BaseModel):
    method = models.ForeignKey(DevelopmentMethod)
    order = models.IntegerField(null=True, blank=True)

    sort_order_field = 'order'

    class Meta:
        verbose_name = _('Development phase')
        verbose_name_plural = _('Development phases')
        ordering = ['method', 'order']


#
# Pages
#

class UserRoleIndex(RelativeURLMixin, Page):
    subpage_types = ['UserRolePage']


class UserRolePage(RelativeURLMixin, Page):
    user_role = models.OneToOneField(UserRole, on_delete=models.PROTECT)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('user_role'),
        StreamFieldPanel('body'),
    ]
    parent_page_types = ['UserRoleIndex']


class KehmetFrontPage(RelativeURLMixin, Page):
    body = StreamField(content_blocks)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    subpage_types = ['KehmetContentPage']


class KehmetContentPageTag(TaggedItemBase):
    content_object = ParentalKey('kehmet.KehmetContentPage', related_name='tagged_items')


class KehmetContentPage(RelativeURLMixin, Page):
    body = StreamField(content_blocks)
    tags = ClusterTaggableManager(through=KehmetContentPageTag, blank=True)
    show_in_submenus = models.BooleanField(verbose_name=_('Show in sub menus'), help_text=_('Page is visible on the submenu'), default=True)

    content_panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('tags'),
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([FieldPanel('show_in_submenus'),], _('Custom page configuration')),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        tag_search_field,
    ]

    parent_page_types = ['KehmetContentPage', 'KehmetFrontPage']
