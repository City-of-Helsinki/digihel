from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin.edit_handlers import RichTextFieldPanel, FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


class CaseKeyword(TaggedItemBase):
    content_object = ParentalKey('helsinkioppii.Case', related_name='cases')


@register_snippet
class SchoolSubject(models.Model):
    subject = models.CharField(
        verbose_name=_('school subject'),
        max_length=128,
        blank=True
    )

    def __str__(self):
        """
        Returns textual representation of the subject.

        :return: Name of the subject.
        :rtype: str
        """
        return self.subject


@register_snippet
class SchoolGrade(models.Model):
    grade = models.CharField(
        verbose_name=_('school grade'),
        max_length=128,
        blank=True
    )

    def __str__(self):
        """
        Returns textual representation of the grade.

        :return: Name of the subject.
        :rtype: str
        """
        return self.grade


class Case(Page):
    template = 'helsinkioppii/case.html'

    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    abstract = models.TextField(verbose_name=_('abstract'))
    content = RichTextField(verbose_name=_('content'))

    # Sidebar content
    school = models.CharField(
        verbose_name=_('school'),
        max_length=128,
        blank=True,
    )
    student_count = models.PositiveSmallIntegerField(
        verbose_name=_('student count'),
        blank=True,
        null=True,
    )
    case_type = models.CharField(
        verbose_name=_('type'),
        max_length=256,
        blank=True
    )
    keywords = ClusterTaggableManager(through=CaseKeyword, blank=True)
    grade = models.ForeignKey(
        'helsinkioppii.SchoolGrade',
        verbose_name=_('school grade'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    subject = models.ForeignKey(
        'helsinkioppii.SchoolSubject',
        verbose_name=_('school subject'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('abstract', classname='full'),
        RichTextFieldPanel('content'),
        FieldPanel('school'),
        FieldPanel('subject', classname='col6'),
        FieldPanel('grade', classname='col6'),
        FieldPanel('student_count', classname='col6'),
        FieldPanel('case_type', classname='col6'),
        FieldPanel('keywords'),
    ]

    @classmethod
    def allowed_parent_page_models(cls):
        from helsinkioppii.models.pages import CaseListPage
        return [CaseListPage]

    @classmethod
    def can_exist_under(cls, parent):
        from helsinkioppii.models.pages import CaseListPage
        return isinstance(parent, CaseListPage)
