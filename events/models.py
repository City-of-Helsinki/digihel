import json, requests
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page, Orderable
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.conf import settings
import django.utils.dateparse as dateparse
from datetime import datetime, time
import pytz
from enumfields import Enum
from enumfields.fields import EnumIntegerField


class DataSources(Enum):
    FACEBOOK = 0
    LINKEDEVENTS = 1


class EventsIndexPage(Page):
    type = _('Events')
    data_source = EnumIntegerField(DataSources, verbose_name=_('Event data source'), default=DataSources.LINKEDEVENTS)
    facebook_page_id = models.CharField(default='1415745085336451', max_length=200)
    linkedevents_params = models.CharField(default='?keyword=yso:p8692', max_length=200)

    content_panels = Page.content_panels + [
        FieldPanel('data_source'),
        FieldPanel('facebook_page_id'),
        FieldPanel('linkedevents_params'),
     ]

    urls = {DataSources.FACEBOOK: "graph.facebook.com/v2.5/",
            DataSources.LINKEDEVENTS: "api.hel.fi/linkedevents/v1/"}

    def _facebook_events(self):
        if not hasattr(settings, 'FACEBOOK_APP_ID') or not hasattr(settings, 'FACEBOOK_APP_SECRET'):
            return []
        events = cache.get('facebook')
        if not events:
            events = []
            # facebook feed returns events latest first
            feed = requests.get('https://' +
                                self.urls[self.data_source] +
                                self.facebook_page_id +
                                '?fields=feed{link,message,object_id}' +
                                '&access_token=' +
                                str(settings.FACEBOOK_APP_ID) + '|' +
                                settings.FACEBOOK_APP_SECRET).json()['feed']['data']

            # filter the events from the feed

            for item in feed:
                if 'link' in item:
                    if 'https://www.facebook.com/events/' in str(item['link']):
                        events.append(item)

            # fetch details for the events

            event_ids = ','.join([event['object_id'] for event in events])
            details = []
            details = requests.get('https://' +
                                self.urls[self.data_source] +
                                '?ids=' + event_ids +
                                '&fields=description,cover,end_time,name,start_time,id,picture,place' +
                                '&access_token=' +
                                str(settings.FACEBOOK_APP_ID) + '|' +
                                settings.FACEBOOK_APP_SECRET).json()
            for event in events:
                event['details'] = details[event['object_id']]
            cache.add('facebook', events, 3600)
        return events

    def _linked_events(self):
        events = cache.get('linkedevents')
        # the methods are assumed to return events latest first
        event_list = requests.get('https://' +
                                  self.urls[self.data_source] +
                                  'event/' +
                                  self.linkedevents_params +
                                  '&sort=-end_time&page_size=100').json()
        events = event_list.get('data')

        # make sure we have all the events fetched

        while event_list.get('meta').get('next'):
            event_list = requests.get(event_list.get('meta').get('next')).json()
            events.extend(event_list.get('data'))
        cache.add('linkedevents', events, 3600)
        return events

    _event_methods = {DataSources.FACEBOOK: _facebook_events,
                     DataSources.LINKEDEVENTS: _linked_events}

    def events(self, future=False):
        try:
            events = self._event_methods[self.data_source](self)
        except (TimeoutError, ConnectionError, LookupError):
            # if the event source is unreachable or down or data is invalid
            events = []
        print(len(events))
        if future:
            # the methods are assumed to return events latest first, reverse the order
            tz = pytz.timezone(settings.TIME_ZONE)
            for event in events:
                # for future filtering, make sure all events have end times not null
                try:
                    end = event['end_time']
                    if not end:
                        event['end_time'] = event['start_time']
                except LookupError:
                    event['end_time'] = event['start_time']
                # check the datetimes first
                start = dateparse.parse_datetime(event['start_time'])
                end = dateparse.parse_datetime(event['end_time'])
                # linkedevents may not have exact times, parse_datetime may fail
                # we have to append time, assume server time zone and convert to utc for filtering
                if not start:
                    start = tz.localize(datetime.combine(dateparse.parse_date(event['start_time']), time()))
                    event['start_time'] = start.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                    print('event start time set as ' + str(event['start_time']))
                if not end:
                    end = tz.localize(datetime.combine(dateparse.parse_date(event['end_time']), time(23,59,59)))
                    event['end_time'] = end.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                    print('event end time set as ' + str(event['end_time']))
            # we want the next event first
            return json.dumps(list(reversed([event for event in events
                                             if dateparse.parse_datetime(event['end_time']) > datetime.now(tz)])))
        return json.dumps(events)
