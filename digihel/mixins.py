from wagtail.wagtailcore.models import Page


class RelativeURLMixin(object):
    def relative_url(self, current_site):
        url_parts = self.get_url_parts()

        if url_parts is None:
            # page is not routable
            return

        site_id, root_url, page_path = url_parts

        return page_path

# Monkeypatch the original relative_url...
Page.relative_url = RelativeURLMixin.relative_url
