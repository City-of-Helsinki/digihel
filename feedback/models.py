from django.db import models
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext, ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import translation

import requests


class Feedback(models.Model):
    url = models.URLField(verbose_name=_('URL of the page where the user was'))
    user_agent = models.CharField(max_length=400, verbose_name=_('The user agent string of the user\'s browser'),
                                  null=True, blank=True)
    subject = models.TextField(blank=True, null=True, verbose_name=_('Subject'))
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Name'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    body = models.TextField(verbose_name=_('Body'))

    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, null=True, blank=True,
                                     on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    class Meta:
        ordering = (('-created_at'),)

    def notify(self):
        if not Notifier.objects.exists():
            return

        notifier = Notifier.objects.first()
        notifier.notify(self)

    def __str__(self):
        return u'{url}: {subject}'.format(url=self.url, subject=self.subject)


class Notifier(models.Model):
    type = models.CharField(max_length=20, choices=(('slack', 'Slack'),))
    url_base = models.CharField(max_length=200)
    language = models.CharField(max_length=20)

    def notify(self, feedback):
        if self.type == 'slack':
            notifier = self.slacknotifier
        else:
            raise NotImplementedError(_('Unsupported notifier type: %s' % self.type))
        notifier.notify(feedback)


class SlackNotifier(Notifier):
    webhook_url = models.URLField()
    channel = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    icon_emoji = models.CharField(max_length=50, null=True, blank=True)
    icon_url = models.URLField(null=True, blank=True)

    def notify(self, feedback):
        attachment = {}
        fields = []
        attachment['fields'] = fields
        attachment['text'] = feedback.body

        # If the feedback refers to a Wagtail Page, add some more
        # information to the Slack notification.
        try:
            Page = apps.get_model('wagtailcore', 'Page')
            klass = feedback.content_type.model_class()
            if issubclass(klass, Page):
                page = Page.objects.get(id=feedback.object_id)
                attachment['title'] = page.title
                attachment['title_link'] = page.full_url
        except (LookupError, ObjectDoesNotExist):
            pass

        attachment['ts'] = int(feedback.created_at.timestamp())
        with translation.override(self.language):
            message = gettext('New feedback received for {url}').format(url=feedback.url)
            if feedback.name:
                fields.append({'title': gettext('Name'), 'value': feedback.name, 'short': False})
            if feedback.user_agent:
                fields.append({'title': gettext('User agent'), 'value': feedback.user_agent, 'short': False})

        data = {'text': message, 'attachments': [attachment]}
        if self.username:
            data['username'] = self.username
        if self.icon_url:
            data['icon_url'] = self.icon_url
        if self.icon_emoji:
            emoji = self.icon_emoji.strip(':')
            data['icon_emoji'] = ':' + emoji + ':'
        if self.channel:
            data['channel'] = self.channel

        resp = requests.post(self.webhook_url, json=data)
        if resp.status_code != 200:
            raise Exception('Slack notify failed with HTTP status %d' % resp.status_code)
