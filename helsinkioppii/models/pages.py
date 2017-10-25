from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.query_utils import Q
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from helsinkioppii.blocks.banner_lift import BannerLiftBlock
from helsinkioppii.blocks.case_lift import CaseLiftBlock
from helsinkioppii.models.cases import Case


class HelsinkiOppiiIndexPage(Page):
    template = 'helsinkioppii/index.html'

    hero_title = models.CharField(
        verbose_name=_('lift title'),
        max_length=256,
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

    banner_lifts = StreamField([
        ('banner', BannerLiftBlock()),
    ], blank=True)

    case_lifts = StreamField([
        ('case', CaseLiftBlock()),
    ], blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        FieldPanel('hero_title'),
        StreamFieldPanel('banner_lifts'),
        StreamFieldPanel('case_lifts'),
    ]


class CaseListPage(Page):
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
        queryset = self.get_case_queryset(form)
        paginated_cases = self.get_paginated_cases(request, queryset)

        context = super(CaseListPage, self).get_context(request, *args, **kwargs)
        context.update({
            'form': form,
            'cases': paginated_cases,
        })
        return context

    def get_case_queryset(self, form):
        """
        Returns Case queryset filtered by given form data.

        :param form: CaseFilterForm instance.
        :return: Case queryset.
        :rtype: django.db.models.query.Queryset
        """
        cases = Case.objects.live()

        if form.is_valid():
            free_text = form.cleaned_data.get('free_text')
            keywords = form.cleaned_data.get('keywords')
            grades = form.cleaned_data.get('grades')
            subjects = form.cleaned_data.get('subjects')

            if free_text:
                q_title = Q(title__icontains=free_text)
                q_abstract = Q(abstract__icontains=free_text)
                q_content = Q(content__icontains=free_text)
                cases = cases.filter(q_title | q_abstract | q_content)
            if keywords:
                cases = cases.filter(keywords__in=keywords)
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
        paginator = Paginator(queryset, 15)  # 15 cases for single page
        page = request.GET.get('page')

        try:
            return paginator.page(page)
        except PageNotAnInteger:
            # Page number not integer. Show first page.
            return paginator.page(1)
        except EmptyPage:
            # Page number out of range. Show last page.
            return paginator.page(paginator.num_pages)
