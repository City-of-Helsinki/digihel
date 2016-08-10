from wagtail.contrib.modeladmin.options import \
    ModelAdmin, ModelAdminGroup, modeladmin_register
from .models import Indicator, FooterLinkSection
from django.utils.html import format_html
from wagtail.wagtailcore import hooks


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
