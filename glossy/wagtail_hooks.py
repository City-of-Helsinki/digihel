from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from .models import Category, Term


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
