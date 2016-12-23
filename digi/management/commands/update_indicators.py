from django.core.management.base import BaseCommand, CommandError
from digi.models import Indicator
from datetime import date, timedelta
import requests

class Command(BaseCommand):
    help = 'Fetches and saves new indicator values'

    def handle(self, *args, **options):
        for indicator in Indicator.objects.all():

            #POPULATION
            if indicator.id == 0:
                pass
                # indicator.value = indicator.value + 1

            #HRI DATASETS
            elif indicator.id == 1:
                try:
                    resp = requests.get('http://hri.fi/api/3/action/package_list')
                    indicator.value = len(resp.json()['result'])
                except Exception as e:
                    # self.stdout.write(self.style.ERROR(e))
                    raise CommandError('Something went wrong while updating HRI datasets indicator, id {}. Retaining previous value {}.'.format(indicator.id, indicator.value))

            #OPEN311 ISSUES
            elif indicator.id == 2:
                try:
                    # week_ago = (date.today() - timedelta(days=7)).isoformat()
                    # resp = requests.get('https://asiointi.hel.fi/palautews/rest/v1/requests.json?status=closed&start_date={}'.format(week_ago))
                    today = date.today().isoformat()
                    resp = requests.get('https://asiointi.hel.fi/palautews/rest/v1/requests.json?status=closed&start_date={}'.format(today))
                    indicator.value = len(resp.json())
                except Exception as e:
                    # self.stdout.write(self.style.ERROR(e))
                    raise CommandError('Something went wrong while updating Open311 issues indicator, id {}. Retaining previous value {}.'.format(indicator.id, indicator.value))

            indicator.save()
            self.stdout.write(self.style.SUCCESS('Successfully updated indicator {}. Value is now {}'.format(indicator.id, indicator.value)))
