from django.db import models
from django.db.models.functions import Lower
from django.utils.six import python_2_unicode_compatible
from django.utils.text import slugify

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index

from digihel.mixins import RelativeURLMixin


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=64)

    def ordered_terms(self):
        return self.terms.all().order_by(Lower('name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'term category'
        verbose_name_plural = 'term categories'


@python_2_unicode_compatible
class Term(index.Indexed, models.Model):
    ctime = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='created on')
    mtime = models.DateTimeField(auto_now=True, editable=False, verbose_name='last modified on')

    category = models.ForeignKey(to=Category, related_name='terms')
    name = models.CharField(max_length=128)
    body = RichTextField(blank=True)
    list_visible = models.BooleanField(default=True, db_index=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        try:
            category_page = self.category.categorypage
        except CategoryPage.DoesNotExist:
            return None

        return '{}#{}'.format(category_page.url, slugify(self.name))


class CategoryPage(RelativeURLMixin, Page):
    category = models.OneToOneField(to=Category, on_delete=models.PROTECT)

    content_panels = Page.content_panels + [
        FieldPanel('category'),
    ]

    def get_term_names(self):
        term_names = self.category.ordered_terms().filter(list_visible=True).values_list('name', flat=True)
        return '\n'.join(term_names)

    search_fields = Page.search_fields + [
        index.SearchField('get_term_names'),
    ]

    def __str__(self):
        return '{} - term category page'.format(self.category.name)

