from django.core.serializers import serialize
from django.http.response import HttpResponse

from .models import Place


def places(request):
    return HttpResponse(
        serialize('geojson', Place.objects.all(), geometry_field='location'),
        content_type="application/json"
    )
