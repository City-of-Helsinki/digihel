from django.core.management.base import BaseCommand

from helsinkioppii.models import Case


class Command(BaseCommand):
    help = 'Adds case theme, grade, and subject to appropriate many-to-many fields.'

    def handle(self, *args, **options):
        # This should be data migration but migrations work in a funny way
        # with many-to-many fields. The values do not get saved to the database
        # when doing the exact same thing in a data migration.
        for case in Case.objects.all():
            if case.theme:
                case.themes.add(case.theme)
            if case.grade:
                case.grades.add(case.grade)
            if case.subject:
                case.subjects.add(case.subject)

            case.save()
