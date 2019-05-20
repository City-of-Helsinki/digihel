from django.core.urlresolvers import reverse
from wagtail.core.models import Page, Site
from wagtail.core.utils import WAGTAIL_APPEND_SLASH


class RelativeURLMixin(object):
    def relative_url(self, current_site, request=None):
        url_parts = self.get_url_parts()

        if url_parts is None:
            # page is not routable
            return

        site_id, root_url, page_path = url_parts

        return page_path

    # Override the method to support the case where we have
    # one Site for testing and another for production.
    def get_url_parts(self, request=None):
        possible_sites = [
            (pk, path, url)
            for pk, path, url in self._get_site_root_paths(request)
            if self.url_path.startswith(path)
        ]

        if not possible_sites:
            return None

        test_site_paths = set([x for x in possible_sites if 'test' in Site.objects.get(id=x[0]).site_name.lower()])
        prod_site_paths = set(possible_sites) - test_site_paths
        if False and self.content_type.app_label == 'kehmet':
            possible_sites = list(test_site_paths)
        else:
            possible_sites = list(prod_site_paths)

        if len(possible_sites) == 0:
            return None

        site_id, root_path, root_url = possible_sites[0]

        if hasattr(request, 'site'):
            for site_id, root_path, root_url in possible_sites:
                if site_id == request.site.pk:
                    break
            else:
                site_id, root_path, root_url = possible_sites[0]

        page_path = reverse(
            'wagtail_serve', args=(self.url_path[len(root_path):],))

        # Remove the trailing slash from the URL reverse generates if
        # WAGTAIL_APPEND_SLASH is False and we're not trying to serve
        # the root path
        if not WAGTAIL_APPEND_SLASH and page_path != '/':
            page_path = page_path.rstrip('/')

        return (site_id, root_url, page_path)


# Monkeypatch the original relative_url...
Page.relative_url = RelativeURLMixin.relative_url
Page.get_url_parts = RelativeURLMixin.get_url_parts
