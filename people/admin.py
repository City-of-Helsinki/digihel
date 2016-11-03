from django.contrib import admin

from .models import Group, Membership


class MembershipAdmin(admin.TabularInline):
    model = Membership


class GroupAdmin(admin.ModelAdmin):
    inlines = [MembershipAdmin]

admin.site.register(Group, GroupAdmin)
