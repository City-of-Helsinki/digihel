from django import template

register = template.Library()


@register.simple_tag
def update_get_parameters(request, parameter, value):
    """
    Copies request GET parameters and sets given parameter
    to given value.

    :return: Updated GET parameters
    :rtype: dict
    """
    get_parameters = request.GET.copy()
    get_parameters[parameter] = value
    return get_parameters.urlencode()
