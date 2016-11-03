from django.utils.html import format_html
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from wagtail.wagtailcore import hooks

from .models import FooterLinkSection, Indicator


class IndicatorAdmin(ModelAdmin):
    model = Indicator
    menu_icon = 'user'


class FooterLinkSectionAdmin(ModelAdmin):
    model = FooterLinkSection
    menu_icon = 'redirect'


class DigiHelAdminGroup(ModelAdminGroup):
    label = "DigiHel"
    items = (IndicatorAdmin, FooterLinkSectionAdmin)

modeladmin_register(DigiHelAdminGroup)


# Enable editing of raw HTML
@hooks.register('insert_editor_js')
def enable_source_editing():
    return format_html(
        """
        <script>
            registerHalloPlugin('hallohtml');
        </script>
        """
    )
