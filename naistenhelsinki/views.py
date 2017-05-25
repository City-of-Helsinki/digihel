
from django.http.response import HttpResponse

from django.core.serializers import serialize

from .models import PlacePage


def places(request):
    return HttpResponse(
        serialize('geojson', PlacePage.objects.all(), geometry_field='location'),
        content_type="application/json")
