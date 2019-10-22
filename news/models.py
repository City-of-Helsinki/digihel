from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from .news import get_news


class NewsIndexPage(RoutablePageMixin, Page):

    @property
    def news_list(self):
        return get_news(self.url)

    class Meta:
        verbose_name = _('News index')

    @route(r'^$')
    def index_view(self, request):
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

        # render the index view
        return render(request, 'news/news_index_page.html', {
            'page': self,
            'news': news_list,
        })

    @route(r'^([\w-]+)/$')
    def news_view(self, request, slug=None):
        selected_news_item = None
        for news_item in self.news_list:
            if news_item.slug == slug:
                selected_news_item = news_item
                break

        if selected_news_item is None:
            raise Http404()

        # render the news view
        return render(request, 'news/news_page.html', {
            'page': self,
            'news_item': selected_news_item
        })
