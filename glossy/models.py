from django.db import models
from django.utils.six import python_2_unicode_compatible
from wagtail.wagtailcore.fields import RichTextField


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'term category'
        verbose_name_plural = 'term categories'


@python_2_unicode_compatible
class Term(models.Model):
    ctime = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='created on')
    mtime = models.DateTimeField(auto_now=True, editable=False, verbose_name='last modified on')

    category = models.ForeignKey(to=Category, related_name='terms')
    name = models.CharField(max_length=128)
    body = RichTextField(blank=True)
    list_visible = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name
