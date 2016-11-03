from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup

from .models import DevelopmentMethod, DevelopmentPhase, UserRole


class UserRoleAdmin(ModelAdmin):
    model = UserRole
    menu_icon = 'user'


class DevelopmentMethodAdmin(ModelAdmin):
    model = DevelopmentMethod


class DevelopmentPhaseAdmin(ModelAdmin):
    model = DevelopmentPhase
    list_display = ('name', 'method')


class KehmetAdminGroup(ModelAdminGroup):
    label = "Kehmet"
    items = (UserRoleAdmin, DevelopmentMethodAdmin, DevelopmentPhaseAdmin)

modeladmin_register(KehmetAdminGroup)
