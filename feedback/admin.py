from django.contrib import admin

from .models import Feedback, SlackNotifier


class FeedbackAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feedback, FeedbackAdmin)


class SlackNotifierAdmin(admin.ModelAdmin):
    pass

admin.site.register(SlackNotifier, SlackNotifierAdmin)
