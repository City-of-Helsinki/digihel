from django.conf.urls import url

from glossy.views import get_terms

urlpatterns = [
    url('^glossy-terms/$', get_terms, name='glossy-terms'),
]
