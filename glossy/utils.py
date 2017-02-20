import json
from collections import defaultdict

from django.db.models.functions import Lower
from django.utils.html import escape
from django.utils.safestring import mark_safe

from glossy.models import Term, Category


def get_tinymce_term_menu():
    # TODO: If there are lots of terms, this should probably be AJAXified.
    terms_by_category = defaultdict(list)
    for term in Term.objects.order_by(Lower('name')).select_related('category__categorypage'):
        url = term.get_absolute_url()
        if url and term.list_visible:
            page = term.category.categorypage
            page_parent = term.category.categorypage.get_parent()
            terms_by_category[term.category_id].append({
                'text': term.name,
                'data_id': page.id,
                'data_parent_id': page_parent.id,
                'url': url,
                'value': term.id,
            })
    category_name_map = dict(
        Category.objects.filter(id__in=terms_by_category.keys()).values_list('id', 'name')
    )
    return [
        {
            'text': category_name_map.get(category_id, str(category_id)),
            'menu': terms,
        }
        for (category_id, terms)
        in sorted(terms_by_category.items())
    ]


def to_js(string):
    return mark_safe(json.dumps(string))


def to_js_primitive(string):
    return mark_safe(json.dumps(escape(string)))
