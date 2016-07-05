from wagtail.contrib.modeladmin.options import \
    ModelAdmin, ModelAdminGroup, modeladmin_register
from .models import Indicator


class IndicatorAdmin(ModelAdmin):
    model = Indicator
    menu_icon = 'user'


class DigiHelAdminGroup(ModelAdminGroup):
    label = "DigiHel"
    items = (IndicatorAdmin,)

modeladmin_register(DigiHelAdminGroup)
