from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin.edit_handlers import RichTextFieldPanel, FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
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

    class Meta:
        ordering = ['pk']

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

    class Meta:
        ordering = ['pk']

    def __str__(self):
        """
        Returns textual representation of the grade.

        :return: Name of the subject.
        :rtype: str
        """
        return self.grade


@register_snippet
class CaseTheme(models.Model):
    theme = models.CharField(
        verbose_name=_('theme'),
        max_length=128,
        blank=True
    )

    class Meta:
        ordering = ['pk']

    def __str__(self):
        """
        Returns textual representation of the theme.

        :return: Name of the theme.
        :rtype: str
        """
        return self.theme


class CaseContact(Orderable):
    case = ParentalKey('helsinkioppii.Case', related_name='contacts')
    person = models.ForeignKey('people.Person', related_name='cases')

    def __str__(self):
        return '{person} as the contact of case {case}'.format(
            person=self.person,
            case=self.case
        )


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
    theme = models.ForeignKey(
        'helsinkioppii.CaseTheme',
        verbose_name=_('theme'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
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
        FieldPanel('theme', classname='col6'),
        FieldPanel('keywords'),
        InlinePanel('contacts', label=_('contacts')),
    ]

    @classmethod
    def allowed_parent_page_models(cls):
        from helsinkioppii.models.pages import CaseListPage
        return [CaseListPage]

    @classmethod
    def allowed_subpage_models(cls):
        return []

    @classmethod
    def can_exist_under(cls, parent):
        from helsinkioppii.models.pages import CaseListPage
        return isinstance(parent, CaseListPage)
