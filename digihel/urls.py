from django.conf import settings
from django.urls import include, path, re_path
from helusers import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from digi.views import sitemap_view
from events.views import event_data
from feedback.views import FeedbackView
from search import views as search_views
from allauth import urls as allauth_urls
from blog import urls as blog_urls

admin.autodiscover()


urlpatterns = [
    re_path(r'^django-admin/', admin.site.urls),

    re_path(r'^admin/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^accounts/', include(allauth_urls)),

    re_path(r'^search/$', search_views.search, name='search'),
    re_path(r'^blogi/', include(blog_urls, namespace="blog")),
    re_path(r'^sivukartta/$', sitemap_view),
    re_path(r'^palaute/$', FeedbackView.as_view(), name='post_feedback'),

    # client endpoints for external API data
    re_path(r'^event_data/', event_data),

    path(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
