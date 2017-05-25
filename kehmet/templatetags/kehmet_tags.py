from django import template
from django.utils.safestring import mark_safe

from ..models import KehmetFrontPage

register = template.Library()


def list_children(page, target_page):

    if getattr(page.specific, 'show_in_submenus', True):
        if page.specific == target_page:
            is_me = True
        else:
            is_me = False
        if target_page.is_descendant_of(page):
            is_parent = True
        else:
            is_parent = False

        children_html = ''
        if is_parent or is_me:
            children = page.get_children().live().public().order_by('path')
            for child in children:
                children_html += list_children(child, target_page)

        if is_me:
            klass = 'active'
        elif is_parent:
            klass = 'open'
        else:
            klass = ''
        if klass:
            klass = ' class="{}"'.format(klass)

        html = '<ul><li{klass}><a href="{url}">{title}</a></li>'\
            .format(url=page.url, title=page.title, klass=klass)
        html += children_html
        html += '</ul>'
        return html
    else:
        return ""


@register.simple_tag
def kehmet_sidebar_page_nav(page):
    parent = page
    while parent is not None and not isinstance(parent.specific, KehmetFrontPage):
        parent = parent.get_parent()
    if parent is None:
        return ''

    html = list_children(parent, page)

    return mark_safe(html)
