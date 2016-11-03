import hashlib

from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.models import Page

from digihel.mixins import RelativeURLMixin
from users.models import User


class Person(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('last_name', 'first_name')

    def get_avatar_url(self, size=40):
        identifier = self.email or hashlib.md5(''.encode('utf8')).hexdigest()
        return 'https://api.hel.fi/avatar/{id}?s={size}'.format(id=identifier, size=size)

    def get_display_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_groups_as_text(self):
        return ', '.join([group.name for group in self.groups.all()])

    def __str__(self):
        return self.get_display_name()


class Group(models.Model):
    name = models.CharField(max_length=100)
    people = models.ManyToManyField(Person, through='people.Membership', blank=True,
                                    related_name='groups')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Membership(models.Model):
    group = models.ForeignKey(Group, db_index=True, related_name='memberships')
    person = models.ForeignKey(Person, db_index=True, related_name='memberships')

    panels = [
        FieldPanel('group'),
        FieldPanel('person')
    ]

    class Meta:
        unique_together = (('group', 'person'),)

    def __str__(self):
        return "{} in {}".format(self.person, self.group)


class PersonIndexPage(RelativeURLMixin, Page):
    groups = models.ManyToManyField(Group)

    def get_groups(self):
        return Group.objects.all()

    def get_people(self):
        return Person.objects.all()
