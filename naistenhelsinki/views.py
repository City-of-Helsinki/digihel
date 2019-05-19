from django.http.response import HttpResponse

from .serializers import PlaceSerializer
from .models import Place


def places(request):
    return HttpResponse(
        PlaceSerializer().serialize(
            queryset=Place.objects.live(),
            geometry_field='location',
            fields=('pk', 'modal_title', 'description', 'image_url'),
        ),
        content_type="application/json"
    )
