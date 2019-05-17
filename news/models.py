from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailcore.models import Page

from .news import get_news_feeds


class NewsIndexPage(Page):

    @property
    def news_list(self):
        return get_news_feeds()

    class Meta:
        verbose_name = _('News index')

    def get_context(self, request, *args, **kwargs):
        context = super(NewsIndexPage, self).get_context(request, *args, **kwargs)

        news_list = self.news_list

        # Pagination
        page = request.GET.get('page')
        page_size = getattr(settings, 'NEWS_PAGINATION_PER_PAGE', 10)

        if page_size is not None:
            paginator = Paginator(news_list, page_size)  # Show 10 blogs per page
            try:
                news_list = paginator.page(page)
            except PageNotAnInteger:
                news_list = paginator.page(1)
            except EmptyPage:
                news_list = paginator.page(paginator.num_pages)

        context['news_list'] = news_list
        return context
