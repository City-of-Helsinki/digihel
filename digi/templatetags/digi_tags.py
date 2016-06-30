from django import template

register = template.Library()


@register.filter
def first_p(value):
    paras = value.split('</p>')
    if len(paras):
        return paras[0] + '</p>'
    return ''
