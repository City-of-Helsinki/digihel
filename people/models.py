import hashlib
from django.db import models

from users.models import User


class Person(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True)

    def get_avatar_url(self, size=40):
        email = self.email or ''
        email_hash = hashlib.md5(email.lower().encode('utf8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?s={}'.format(email_hash, size)

    def get_display_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.get_display_name()
