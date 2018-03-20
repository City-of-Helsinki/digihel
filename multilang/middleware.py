from django.utils import translation

from multilang.utils import get_requested_page_language_code


class PageLanguageMiddleware(object):
    """
    Middleware that activates the used language based on the requested
    url language. Defaults to browser language.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        page_language = get_requested_page_language_code(request)

        if page_language:
            translation.activate(page_language)

        return self.get_response(request)
