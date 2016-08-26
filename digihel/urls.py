from django.conf.urls import include, url
from django.conf import settings
from helusers import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from search import views as search_views
from digi.views import sitemap_view
from feedback.views import FeedbackView

admin.autodiscover()


urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^blogi/', include('blog.urls', namespace="blog")),
    url(r'^sivukartta/$', sitemap_view),
    url(r'^palaute/$', FeedbackView.as_view(), name='post_feedback'),

    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
