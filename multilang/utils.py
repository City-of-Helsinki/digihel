from django.conf import settings
from django.utils import translation


def get_request_path_parts(request):
    """
    Return list of request path parts.

    >>> request.path = '/en/foo/bar'
    >>> PageLanguageMiddleware._get_request_path_parts(request)
    ['en', 'foo', 'bar']

    :param request: django.http.request.HttpRequest object
    :return: List of request path parts
    :rtype: list
    """
    return list(filter(None, request.path.split('/')))


def get_available_languages():
    """
    Return list of available language codes determined in Django
    project settings.
    """
    return [language[0] for language in settings.LANGUAGES]


def get_requested_page_language_code(request, default_to_browser_language=False):
    """
    Return the the language code for the requested page. Returns None
    if the page has no language.
    """
    available_languages = get_available_languages()
    language = None

    if default_to_browser_language:
        language = translation.get_language_from_request(request)

    path_parts = get_request_path_parts(request)

    if path_parts and path_parts[0] in available_languages:
        language = path_parts[0]

    return language
