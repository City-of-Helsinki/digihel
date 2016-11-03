# -*- coding: utf-8 -*-
import pytest
from blog.models import BlogIndexPage
from wagtail.wagtailcore.models import Page, Site

from digi.models import FrontPage


def root_page():
    return Page.objects.get(depth=1)


@pytest.mark.django_db
@pytest.fixture
def home_page():
    rp = root_page()
    rp.get_children().delete()
    hp = root_page().add_child(instance=FrontPage(title='Test Home', live=True))
    site = Site(hostname='localhost', is_default_site=True, port=80, site_name='Test site',
                root_page=hp)
    site.save()
    return hp


@pytest.mark.django_db
@pytest.fixture
def index_pages():
    home = home_page()
    blog_index = home.add_child(instance=BlogIndexPage(title='Test Blog Index', live=True))

    return [home, blog_index]
