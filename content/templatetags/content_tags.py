from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page

def has_menu_children(page):
    return page.get_children().live().in_menu().exists()

# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


def list_children(page, target_page):
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


@register.simple_tag
def sidebar_page_nav(page):
    parent = page
    while parent is not None and not parent.show_in_menus:
        print(parent)
        print(parent.show_in_menus)
        parent = parent.get_parent()
    if parent is None:
        return None

    html = list_children(parent, page)

    return mark_safe(html)
