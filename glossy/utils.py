import json
from collections import defaultdict

from django.utils.html import escape
from django.utils.safestring import mark_safe

from glossy.models import Term, Category


def get_tinymce_term_menu():
    # TODO: If there are lots of terms, this should probably be AJAXified.
    terms_by_category = defaultdict(list)
    for term_id, category_id, name in Term.objects.all().values_list('id', 'category_id', 'name'):
        terms_by_category[category_id].append({
            'text': name,
            'value': term_id,
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
