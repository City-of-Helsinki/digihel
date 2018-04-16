from blog.models import BlogPage
from django import template
from django.conf import settings

from digi.templatetags.digi_tags import first_p
from events.models import EventsIndexPage

register = template.Library()


@register.simple_tag
def get_index_blog_lifts():
    count = settings.HELSINKI_OPPII_INDEX_BLOG_LIFT_COUNT
    return BlogPage.objects.live().order_by('-first_published_at')[:count]


@register.filter
def first_rich_text_paragraph(rich_text):
    wrap_start = '<div class="rich-text">'
    wrap_end = '</div>'

    # Strip the wrapper element start and end if it exists
    if rich_text.startswith(wrap_start):
        rich_text = rich_text[len(wrap_start):]
    if rich_text.endswith(wrap_end):
        n = len(wrap_end) * -1
        rich_text = rich_text[:n]

    return first_p(rich_text)


@register.simple_tag
def get_event_index():
    return EventsIndexPage.objects.live().first()
