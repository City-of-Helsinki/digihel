from django.apps import AppConfig

from search.patches import patch_blog_page_search


class SearchAppConfig(AppConfig):
    name = 'search'

    def ready(self):
        patch_blog_page_search()
