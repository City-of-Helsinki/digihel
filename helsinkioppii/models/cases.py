from django.db import models
from django.forms import model_to_dict
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import RichTextFieldPanel, FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailsnippets.models import register_snippet

from helsinkioppii.utils import get_substrings


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


class Case(RoutablePageMixin, Page):
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

    # Leave this now for legacy. Not shown or used in admin ui
    content = RichTextField(verbose_name=_('content'), blank=True)

    # Content field split in sections to guide consistent formatting
    content_objectives = RichTextField(verbose_name=_('Objectives'), blank=True)
    content_what = RichTextField(verbose_name=_('What was done'), blank=True)
    content_how = RichTextField(verbose_name=_('How it was done'), blank=True)
    content_who = RichTextField(verbose_name=_('Who participated'), blank=True)
    content_evaluation = RichTextField(verbose_name=_('How the learning was evaluated'), blank=True)
    content_materials = RichTextField(verbose_name=_('What materials were useed'), blank=True)
    content_pros = RichTextField(verbose_name=_('Pros'), blank=True)
    content_cons = RichTextField(verbose_name=_('Cons'), blank=True)

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
    themes = ParentalManyToManyField(
        'helsinkioppii.CaseTheme',
        verbose_name=_('themes'),
        blank=True,
        related_name="+"
    )
    keywords = ClusterTaggableManager(through=CaseKeyword, blank=True)
    grades = ParentalManyToManyField(
        'helsinkioppii.SchoolGrade',
        verbose_name=_('school grades'),
        blank=True,
        related_name="+"
    )
    subjects = ParentalManyToManyField(
        'helsinkioppii.SchoolSubject',
        verbose_name=_('school subjects'),
        blank=True,
        related_name="+"
    )

    # Deprecated foreign key relationships
    # TODO: Remove after a month or two (around April/May 2018). Check
    #       that `./ manage.py update_case_m2m_with_fk_values` has been
    #       ran in production before removing these fields.
    subject = models.ForeignKey(
        'helsinkioppii.SchoolSubject',
        verbose_name=_('school subject'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    grade = models.ForeignKey(
        'helsinkioppii.SchoolGrade',
        verbose_name=_('school grade'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    theme = models.ForeignKey(
        'helsinkioppii.CaseTheme',
        verbose_name=_('theme'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    # Legal
    cc_license = models.BooleanField(
        verbose_name=_('Creative Commons license'),
        default=False,
        help_text=_('I am licensing this content under Creative Commons license.')
    )
    photo_permission = models.BooleanField(
        verbose_name=_('Photo permission'),
        default=False,
        help_text=_(
            'I have the permission to publish the images associated to this case. I have the permission to use the '
            'images or I have the copyright to the images. People have given permission to publish the images they '
            'appear in.'
        )
    )

    # Meta
    draft = models.BooleanField(
        verbose_name=_('draft'),
        default=False,
        help_text=_('Hidden draft flag used with frontend editing.')
    )

    # Group separated content fields in admin ui
    case_content_panel = MultiFieldPanel(
        [
            RichTextFieldPanel('content_objectives'),
            RichTextFieldPanel('content_what'),
            RichTextFieldPanel('content_how'),
            RichTextFieldPanel('content_who'),
            RichTextFieldPanel('content_evaluation'),
            RichTextFieldPanel('content_materials'),
            RichTextFieldPanel('content_pros'),
            RichTextFieldPanel('content_cons'),
        ],
        heading=_('Case description'),
        classname="collapsible"
    )

    # Group meta fields in admin ui
    sidebar_content_panel = MultiFieldPanel(
        [
            FieldPanel('school'),
            FieldPanel('subjects', classname='col6'),
            FieldPanel('grades', classname='col6'),
            FieldPanel('student_count', classname='col6'),
            FieldPanel('themes', classname='col6'),
            FieldPanel('keywords'),
            InlinePanel('contacts', label=_('contacts')),
        ],
        heading=_('Case meta'),
        classname='collapsible collapsed'
    )

    deprecated_relations_panel = MultiFieldPanel(
        [
            FieldPanel('subject', classname='col4'),
            FieldPanel('grade', classname='col4'),
            FieldPanel('theme', classname='col4'),
        ],
        heading=_('Deprecated relationships'),
        classname='collapsible collapsed'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('abstract', classname='full'),
        sidebar_content_panel,
        deprecated_relations_panel,
        case_content_panel,
        FieldPanel('draft')
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

    def _is_user_action_allowed(self, user):
        """
        Check that current user has permission to access frontend management
        views for Case instance. Original creator (owner) of the Case and staff
        users have permissions.
        """
        return user == self.owner or user.is_staff

    def _get_relative_route_path(self, route):
        """
        Get a relative path of the Case instance and concatenate given route
        to the end of it.

        :param route: Route string.
        :return: Relative path for given route.
        """
        return '{page_url}{route}'.format(
            page_url=self.get_url(),
            route=route
        )

    @property
    def update_view_path(self):
        """
        Return relative path for referring the edit view of this page.
        """
        return self._get_relative_route_path('edit/')

    @property
    def publish_view_path(self):
        """
        Return relative path for referring the publish view of this page.
        """
        return self._get_relative_route_path('publish/')

    @property
    def unpublish_view_path(self):
        """
        Return relative path for referring the unpublish view of this page.
        """
        return self._get_relative_route_path('unpublish/')

    @property
    def delete_view_path(self):
        """
        Return relative path for referring the unpublish view of this page.
        """
        return self._get_relative_route_path('delete/')

    def assign_values_from_form_data(self, form):
        """
        Updates the relevant field values from form data.

        :param form: Validated CaseForm instance.
        """
        # Fields that require special handling before value is assigned to object.
        special_fields = [
            'image', 'image_title', 'new_themes', 'new_grades', 'new_subjects', 'keywords',
        ]

        for field, value in form.cleaned_data.items():
            if field not in special_fields:
                setattr(self, field, value)

        self.keywords.clear()  # Clear old keywords.

        if form.cleaned_data['image']:
            image = Image.objects.create(
                file=form.cleaned_data['image'],
                title=form.cleaned_data['image_title']
            )
            self.image = image

        new_themes = form.cleaned_data.get('new_themes')
        if new_themes:
            for theme in get_substrings(new_themes):
                theme_instance, created = CaseTheme.objects.get_or_create(theme=theme)
                self.themes.add(theme_instance)

        new_grades = form.cleaned_data.get('new_grades')
        if new_grades:
            for grade in get_substrings(new_grades):
                grade_instance, created = SchoolGrade.objects.get_or_create(grade=grade)
                self.grades.add(grade_instance)

        new_subjects = form.cleaned_data.get('new_subjects')
        if new_subjects:
            for subject in get_substrings(new_subjects):
                subject_instance, created = SchoolSubject.objects.get_or_create(subject=subject)
                self.subjects.add(subject_instance)

        keywords = form.cleaned_data.get('keywords')
        if keywords:
            tag_model = CaseKeyword.tag_model()
            for keyword in get_substrings(keywords):
                keyword_instance, created = tag_model.objects.get_or_create(name=keyword)
                self.keywords.add(keyword_instance)

    @route(r'^edit/$')
    def update_view(self, request):
        if not self._is_user_action_allowed(request.user):
            return HttpResponseForbidden()

        from helsinkioppii.forms import CaseForm

        if request.method == 'GET':
            initial_values = model_to_dict(self)
            initial_values['keywords'] = str.join('; ', [kw.name for kw in self.keywords.all()])
            return render(request, 'helsinkioppii/edit_case.html', {
                'page': self,
                'draft': self.draft,
                'form_action_url': self.update_view_path,
                'form': CaseForm(initial=initial_values),
            })

        if request.method == 'POST':
            form = CaseForm(request.POST, request.FILES)
            if form.is_valid():
                self.assign_values_from_form_data(form)
                self.save()
                return redirect(self.get_url())

            return render(request, 'helsinkioppii/edit_case.html', {
                'page': self,
                'draft': self.draft,
                'form_action_url': self.update_view_path,
                'form': form,
            })

        return HttpResponseBadRequest()

    @route(r'^publish/$')
    def publish_view(self, request):
        if not self._is_user_action_allowed(request.user):
            return HttpResponseForbidden()

        self.draft = False
        self.save()

        return redirect(self.get_url())

    @route(r'^unpublish/$')
    def unpublish_view(self, request):
        if not self._is_user_action_allowed(request.user):
            return HttpResponseForbidden()

        self.draft = True
        self.save()

        return redirect(self.get_url())

    @route(r'^delete/$')
    def delete_view(self, request):
        if not self._is_user_action_allowed(request.user):
            return HttpResponseForbidden()

        case_list_page = self.get_parent()

        self.draft = True  # Flag the Case as draft so it's not published immediately if recovered by admin.
        self.unpublish(commit=True)

        return redirect(case_list_page.get_url())
