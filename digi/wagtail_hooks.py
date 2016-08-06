from wagtail.contrib.modeladmin.options import \
    ModelAdmin, ModelAdminGroup, modeladmin_register
from .models import Indicator, FooterLinkSection


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
