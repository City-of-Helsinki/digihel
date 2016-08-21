from django.utils.translation import ugettext_lazy as _
from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailsearch import index
from content.models import content_blocks


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

class UserRoleIndex(Page):
    subpage_types = ['UserRolePage']


class UserRolePage(Page):
    user_role = models.OneToOneField(UserRole, on_delete=models.PROTECT)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('user_role'),
        StreamFieldPanel('body'),
    ]
    parent_page_types = ['UserRoleIndex']


class KehmetFrontPage(Page):
    body = StreamField(content_blocks)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    subpage_types = ['KehmetContentPage']


class KehmetContentPage(Page):
    body = StreamField(content_blocks)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    parent_page_types = ['KehmetContentPage', 'KehmetFrontPage']
