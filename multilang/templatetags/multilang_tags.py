from django import template
from django.conf import settings
from wagtail.wagtailcore.models import Page

from multilang.utils import get_requested_page_language_code

register = template.Library()


@register.simple_tag(takes_context=True)
def get_page_language_code(context):
    return get_requested_page_language_code(context['request'])


@register.simple_tag(takes_context=True)
def get_language_root_url(context):
    lang_code = get_page_language_code(context)
    return '/%s/' % lang_code


@register.assignment_tag(takes_context=True)
def get_language_index_page(context):
    lang_code = get_requested_page_language_code(context['request'])
    return Page.objects.get(slug=lang_code)


@register.simple_tag
def get_page_language_link(page, lang_code):
    try:
        linked_page = page.get_linked_page_for_language_code(lang_code)
    except AttributeError:
        # Page is not translatable (it doesn't subclass TranslatablePageMixin)
        linked_page = None

    if linked_page:
        return linked_page.url

    return '/%s/' % lang_code


@register.simple_tag
def get_language_options():
    options = []
    for language in settings.LANGUAGES:
        options.append({
            'language_code': language[0],
            'verbose_name': language[1],
        })
    return options
