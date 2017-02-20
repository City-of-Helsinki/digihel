from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from wagtail.wagtailcore import hooks

from glossy.models import Category, Term
from glossy.utils import get_tinymce_term_menu, to_js, to_js_primitive


class TermModelAdmin(ModelAdmin):
    model = Term
    menu_icon = 'doc-full-inverse'
    list_display = ('name', 'category', 'list_visible')
    list_filter = ('category', 'list_visible')
    search_fields = ('name', 'category__name')


class CategoryModelAdmin(ModelAdmin):
    model = Category
    menu_icon = 'folder-open-inverse'
    list_display = ('name',)
    search_fields = ('name',)


class GlossyAdminGroup(ModelAdminGroup):
    menu_label = 'Terms'
    menu_icon = 'folder-open-inverse'  # change as required
    items = (CategoryModelAdmin, TermModelAdmin)


modeladmin_register(GlossyAdminGroup)


@hooks.register('insert_tinymce_js')
def tinymce_term_span_js():
    return format_html(
        '<script>var TERMLINK_MENU = {};\nregisterMCEPlugin("termlink", {});</script>',
        to_js(get_tinymce_term_menu()),
        to_js_primitive(static('js/tinymce-termlink.js')),
    )
