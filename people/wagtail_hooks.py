from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Person


class PersonAdmin(ModelAdmin):
    model = Person
    menu_label = _("People")
    menu_icon = 'user'

modeladmin_register(PersonAdmin)
