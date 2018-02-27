from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.db.models.query_utils import Q
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from helsinkioppii.blocks.banner_lift import BannerLiftBlock
from helsinkioppii.blocks.case_lift import CaseLiftBlock
from helsinkioppii.blocks.training_lift import TrainingLiftBlock
from helsinkioppii.models.cases import Case


class PageOutOfRangeException(Exception):
    pass


class HelsinkiOppiiIndexPage(Page):
    template = 'helsinkioppii/index.html'

    hero_content = RichTextField(
        verbose_name=_('hero content'),
        blank=True,
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('hero image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    # Banner section
    banner_section_title = models.CharField(
        verbose_name=_('banner section title'),
        max_length=255,
        blank=True,
    )
    banner_section_description = RichTextField(
        verbose_name=_('banner section description'),
        blank=True,
    )
    banner_lifts = StreamField([
        ('banner', BannerLiftBlock()),
    ], blank=True)

    # Case section
    case_section_title = models.CharField(
        verbose_name=_('case section title'),
        max_length=255,
        blank=True,
    )
    case_section_description = RichTextField(
        verbose_name=_('case section description'),
        blank=True,
    )
    case_lifts = StreamField([
        ('case', CaseLiftBlock()),
    ], blank=True)

    # Social section
    social_section_title = models.CharField(
        verbose_name=_('social section title'),
        max_length=255,
        blank=True,
    )
    social_section_description = RichTextField(
        verbose_name=_('social section description'),
        blank=True,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        FieldPanel('hero_content'),
        FieldPanel('banner_section_title'),
        FieldPanel('banner_section_description'),
        StreamFieldPanel('banner_lifts'),
        FieldPanel('case_section_title'),
        FieldPanel('case_section_description'),
        StreamFieldPanel('case_lifts'),
        FieldPanel('social_section_title'),
        FieldPanel('social_section_description'),
    ]


class CaseListPage(RoutablePageMixin, Page):
    template = 'helsinkioppii/case_list_page.html'

    @classmethod
    def allowed_subpage_models(cls):
        return [Case]

    def get_context(self, request, *args, **kwargs):
        """
        Returns template context data.

        :param request: HTTP request data.
        :return: Template context data.
        :rtype: dict
        """
        from helsinkioppii.forms import CaseFilterForm

        form = CaseFilterForm(request.GET)
        queryset = self.get_case_queryset(form, request.user.pk)
        paginated_cases = self.get_paginated_cases(request, queryset)

        context = super(CaseListPage, self).get_context(request, *args, **kwargs)
        context.update({
            'form': form,
            'cases': paginated_cases,
        })
        return context

    def get_case_queryset(self, form, user_pk=None):
        """
        Returns Case queryset filtered by given form data.

        :param form: CaseFilterForm instance.
        :param user_pk: Primary key of authenticated user.
        :return: Case queryset.
        :rtype: django.db.models.query.Queryset
        """
        cases = Case.objects.live().filter(draft=False)

        if user_pk:
            # Include drafts made by current user to the case list.
            visible_drafts = Case.objects.live().filter(draft=True, owner__pk=user_pk)
            cases = cases.union(visible_drafts)

        cases = cases.order_by('-first_published_at')

        if form.is_valid():
            free_text = form.cleaned_data.get('free_text')
            themes = form.cleaned_data.get('themes')
            grades = form.cleaned_data.get('grades')
            subjects = form.cleaned_data.get('subjects')

            if free_text:
                q_title = Q(title__icontains=free_text)
                q_abstract = Q(abstract__icontains=free_text)
                q_content = Q(content__icontains=free_text)
                cases = cases.filter(q_title | q_abstract | q_content)
            if themes:
                cases = cases.filter(theme__in=themes)
            if grades:
                cases = cases.filter(grade__in=grades)
            if subjects:
                cases = cases.filter(subject__in=subjects)

        return cases.distinct()

    def get_paginated_cases(self, request, queryset):
        """
        Apply pagination for the given case queryset.

        :param request: HTTP request.
        :param queryset: Case queryset.
        :return: Case pagination page.
        :rtype: django.core.paginator.Page
        """
        paginator = Paginator(queryset, settings.HELSINKI_OPPII_CASES_PER_PAGE)
        page = request.GET.get('page')

        try:
            return paginator.page(page)
        except PageNotAnInteger:
            # Page number not integer. Show first page.
            return paginator.page(1)
        except EmptyPage:
            # Page number out of range.
            raise PageOutOfRangeException

    def serve(self, request, *args, **kwargs):
        try:
            return super(CaseListPage, self).serve(request, *args, **kwargs)
        except PageOutOfRangeException:
            return HttpResponseBadRequest()

    @property
    def create_view_path(self):
        """
        Return relative path for referring the create view of this page.
        """
        return '{page_url}new/'.format(
            page_url=self.get_url()
        )

    @route(r'^new/$')
    def create_view(self, request):
        if not request.user.pk:
            # Unauthenticated users are not allowed to create new Cases.
            return HttpResponseForbidden()

        from helsinkioppii.forms import CaseForm

        if request.method == 'GET':
            return render(request, 'helsinkioppii/create_case.html', {
                'page': self,
                'draft': True,
                'form_action_url': self.create_view_path,
                'form': CaseForm()
            })

        if request.method == 'POST':
            form = CaseForm(request.POST, request.FILES)
            if form.is_valid():
                case = Case()

                case.assign_values_from_form_data(form)
                case.owner = request.user
                case.draft = True  # New cases initially created as drafts.

                self.add_child(instance=case)

                return redirect(case.get_url())

            return render(request, 'helsinkioppii/create_case.html', {
                'page': self,
                'draft': True,  # New cases initially created as drafts.
                'form_action_url': self.create_view_path,
                'form': form,
            })

        # Only GET and POST are allowed
        return HttpResponseBadRequest()


class TrainingIndexPage(Page):
    template = 'helsinkioppii/training_index.html'

    hero_content = RichTextField(
        verbose_name=_('hero content'),
        blank=True,
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('hero image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    # Training section
    training_section_title = models.CharField(
        verbose_name=_('training section title'),
        max_length=255,
        blank=True,
    )
    training_section_description = RichTextField(
        verbose_name=_('training section description'),
        blank=True,
    )
    training_lifts = StreamField([
        ('training', TrainingLiftBlock()),
    ], blank=True)

    # Banner section
    banner_section_title = models.CharField(
        verbose_name=_('banner section title'),
        max_length=255,
        blank=True,
    )
    banner_section_description = RichTextField(
        verbose_name=_('banner section description'),
        blank=True,
    )
    banner_lifts = StreamField([
        ('banner', BannerLiftBlock()),
    ], blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        FieldPanel('hero_content'),
        FieldPanel('banner_section_title'),
        FieldPanel('banner_section_description'),
        StreamFieldPanel('banner_lifts'),
        FieldPanel('training_section_title'),
        FieldPanel('training_section_description'),
        StreamFieldPanel('training_lifts'),
    ]
