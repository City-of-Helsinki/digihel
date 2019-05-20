import re
from collections import Sequence

from bs4 import BeautifulSoup

from django import template
from django.utils.safestring import mark_safe

from wagtail.core.blocks.base import BoundBlock
from wagtail.core.rich_text import RichText
from wagtail.core.models import Site

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return Site.find_for_request(context['request']).root_page


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

    site = context['request'].site
    # if 'test' not in site.site_name.lower():
    #    menuitems = [x for x in menuitems if x.content_type.app_label != 'kehmet']

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
        .format(url=page.relative_url(page.get_site()),
                title=page.title, klass=klass)
    html += children_html
    html += '</ul>'
    return html


@register.simple_tag
def sidebar_page_nav(page):
    parent = page
    while parent is not None and not parent.show_in_menus:
        parent = parent.get_parent()
    if parent is None:
        return ''

    html = list_children(parent, page)

    return mark_safe(html)


class TableOfContentsNode(template.Node):
    def __init__(self, html_accessor, toc_var_name):
        self.html_accessor = html_accessor
        self.html_var = template.Variable(html_accessor)
        self.toc_var_name = toc_var_name

    def render(self, context):

        blocks = self.html_var.resolve(context)

        if not isinstance(blocks, Sequence):
            blocks = [blocks]

        headings_and_anchors = []
        toc_anchor_count = 1

        for block in blocks:
            if (not isinstance(block, BoundBlock) or not
            isinstance(block.value, RichText)):
                continue
            soup = BeautifulSoup(block.value.source)
            h2_tags = soup.find_all('h2')

            if not h2_tags:
                continue

            for t in h2_tags:
                # let's not add empty headings to table of contents
                if not t.string.strip():
                    continue
                anchor = 'toc-{}'.format(toc_anchor_count)
                headings_and_anchors.append((t.string, anchor))
                t.insert_before(soup.new_tag('span', id=anchor, **{'class':'toc-anchor'}))
                toc_anchor_count += 1

            new_source = str(soup)
            # See wagtail.core.rich_text expand_db_html and
            # replace_embed_tag - if the embed tag doesn't close itself,
            # replace_embed_tag doesn't recognize it, and can't replace it
            # with img tag
            new_source = new_source.replace('></embed>', '/>')
            block.value.source = new_source


        context[self.toc_var_name] = headings_and_anchors

        return ''

    def __unicode__(self):
        return u'String repr'


def do_table_of_contents(parser, token):
    """
    Use like this:
    {% do_table_of_contents <context variable> as
    <table of contents item list> %}

    This takes a WagTail BoundBlock or a list of them, and for each block with
    RichText value, goes through H2 elements, and adds an anchor to them. It
    puts out a list or headings and anchors, as in
    [('Heading 1', 'toc-1'), ...], which can be used to render a table of
    contents in the template.
    """
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents.split()[0]
        )
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" %
                                           tag_name)
    format_string, var_name = m.groups()

    return TableOfContentsNode(format_string, var_name)


register.tag('do_table_of_contents', do_table_of_contents)