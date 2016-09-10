from django import template

register = template.Library()


@register.simple_tag
def person_avatar(person, size=80):
    return person.get_avatar_url(size)
