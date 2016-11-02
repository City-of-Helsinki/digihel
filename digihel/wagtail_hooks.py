import json

from django.templatetags.static import static
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from wagtail.wagtailcore import hooks


def to_js_primitive(string):
    return mark_safe(json.dumps(escape(string)))


@hooks.register('insert_tinymce_js')
def tinymce_term_span_js():
    return format_html(
        '<script>registerMCEPlugin("termspan", {});</script>',
        to_js_primitive(static('js/tinymce-termspan.js')),
    )
