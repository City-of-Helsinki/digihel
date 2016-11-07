from django.http.response import JsonResponse

from glossy.models import Term


def get_terms(request):
    """
    Get term definitions for the given IDs.

    Ids to be passed in comma-separated in the `ids` query string argument.

    :param request: HTTP Request
    :type request: django.http.HttpRequest
    :return: JSON response
    """
    term_ids = [int(term_id) for term_id in request.GET.get('ids', '0').split(',')]
    term_data = Term.objects.filter(id__in=term_ids).values('id', 'name', 'body')
    return JsonResponse({term['id']: term for term in term_data})
