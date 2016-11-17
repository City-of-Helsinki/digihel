from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from events.models import EventsIndexPage

# Create your views here.


def event_data(request):
    future = request.GET.get('future', 'False')
    try:
        if future.lower() == 'True'.lower():
            data = EventsIndexPage.objects.get().events(future=True)
        else:
            data = EventsIndexPage.objects.get().events()
    except EventsIndexPage.DoesNotExist:
        return HttpResponseNotFound({'No events index page could be found. Please create one in Wagtail Admin.'})
    return HttpResponse(data)
