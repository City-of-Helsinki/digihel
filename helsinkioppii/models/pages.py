from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.db.models.query_utils import Q
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, PageChooserPanel
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from helsinkioppii.blocks.banner_lift import BannerLiftBlock
from helsinkioppii.blocks.case_lift import CaseLiftBlock
from helsinkioppii.blocks.training_lift import TrainingLiftBlock
from helsinkioppii.models.cases import Case
from multilang.models import TranslatablePageMixin
from multilang.utils import get_available_languages


class PageOutOfRangeException(Exception):
    pass


class HelsinkiOppiiIndexPage(TranslatablePageMixin, Page):
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

    youtube_embed = models.URLField(
        verbose_name=_('Youtube video embed'),
        blank=True,
        null=False,
        max_length=255,
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
        # FieldPanel('banner_section_title'),
        # FieldPanel('banner_section_description'),
        # StreamFieldPanel('banner_lifts'),
        FieldPanel('youtube_embed'),
        FieldPanel('case_section_title'),
        FieldPanel('case_section_description'),
        StreamFieldPanel('case_lifts'),
        FieldPanel('social_section_title'),
        FieldPanel('social_section_description'),
    ]
    promote_panels = TranslatablePageMixin.panels + Page.promote_panels

    @classmethod
    def allowed_subpage_models(cls):
        from content.models import ContentPage, LinkedContentPage
        from blog.models import BlogIndexPage

        return [
            ContentPage, LinkedContentPage, CaseListPage,
            TrainingIndexPage, BlogIndexPage, PageGroupPage,
        ]

    def clean(self):
        available_languages = get_available_languages()
        if self.slug not in available_languages:
            language_options = available_languages.join(', ')
            raise ValueError(
                _('Slug has to be one of the available site languages. Options: {options}').format(
                    options=language_options
                )
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class CaseListPage(RoutablePageMixin, TranslatablePageMixin, Page):
    template = 'helsinkioppii/case_list_page.html'

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('hero image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    lead_text = RichTextField(
        verbose_name=_('lead text'),
        blank=True,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        FieldPanel('lead_text'),
    ]

    promote_panels = TranslatablePageMixin.panels + Page.promote_panels

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
        visible_drafts = Case.objects.none()

        if user_pk:
            # Include drafts made by current user to the case list.
            visible_drafts = Case.objects.live().filter(draft=True, owner__pk=user_pk)

        if form.is_valid():
            free_text = form.cleaned_data.get('free_text')
            themes = form.cleaned_data.get('themes')
            grades = form.cleaned_data.get('grades')
            subjects = form.cleaned_data.get('subjects')

            if free_text:
                q_title = Q(title__icontains=free_text)
                q_abstract = Q(abstract__icontains=free_text)
                cases = cases.filter(q_title | q_abstract)
                if visible_drafts:
                    visible_drafts = visible_drafts.filter(q_title | q_abstract)

            if themes:
                cases = cases.filter(themes__in=themes)
                if visible_drafts:
                    visible_drafts = visible_drafts.filter(themes__in=themes)

            if grades:
                cases = cases.filter(grades__in=grades)
                if visible_drafts:
                    visible_drafts = visible_drafts.filter(grades__in=grades)

            if subjects:
                cases = cases.filter(subjects__in=subjects)
                if visible_drafts:
                    visible_drafts = visible_drafts.filter(subjects__in=subjects)

        if visible_drafts:
            cases = cases.union(visible_drafts)

        cases = cases.order_by('-first_published_at')

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

                # Save case and make it a child for current CaseListPage instance.
                self.add_child(instance=case)

                # Create related objects from form data.
                case.update_gallery_images_from_form_data(form)
                case.update_attachments_from_form_data(form)
                case.update_sidebar_links_from_form_data(form)

                return redirect(case.get_url())

            return render(request, 'helsinkioppii/create_case.html', {
                'page': self,
                'draft': True,  # New cases initially created as drafts.
                'form_action_url': self.create_view_path,
                'form': form,
            })

        # Only GET and POST are allowed
        return HttpResponseBadRequest()


class TrainingIndexPage(TranslatablePageMixin, Page):
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

    promote_panels = TranslatablePageMixin.panels + Page.promote_panels

    @classmethod
    def allowed_subpage_models(cls):
        from content.models import ContentPage, LinkedContentPage
        from digi.models import ThemePage

        return [ContentPage, LinkedContentPage, ThemePage]


class PageGroupPage(TranslatablePageMixin, Page):
    template = 'helsinkioppii/page_group_page.html'

    redirect_to = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        PageChooserPanel('redirect_to'),
    ]
    promote_panels = TranslatablePageMixin.panels + Page.promote_panels

    @classmethod
    def allowed_subpage_models(cls):
        from content.models import ContentPage, LinkedContentPage
        from digi.models import ThemePage

        return [ContentPage, LinkedContentPage, ThemePage]

    def serve(self, request, *args, **kwargs):
        if self.redirect_to:
            return HttpResponseRedirect(self.redirect_to.url)
        return super().serve(request, *args, **kwargs)
