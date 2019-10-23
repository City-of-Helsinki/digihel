import re

import feedparser
from django.conf import settings
from django.core.cache import cache


def get_news_cached(base_url):
    cache_key = 'news_cache_key'
    news = cache.get(cache_key)
    if not news:
        news = get_news(base_url)
        cache.set(cache_key, news, settings.NEWS_FEED_CACHE_TIMEOUT)
    return news


def get_news(base_url):
    img_re = re.compile(r'<img.*?src=["\']+(.*?)["\']+/>')
    slug_re = re.compile(r'([\w-]+$)')
    entries = get_news_feeds()
    for entity in entries:
        img_search = img_re.search(entity.description)
        try:
            entity.image = img_search.group(1)
            entity.parsed_description = img_re.sub('', entity.description)
        except AttributeError:
            entity.parsed_description = entity.description

        try:
            entity.slug = slug_re.search(entity.link).group(1)
            entity.real_link = base_url + entity.slug if base_url and entity.slug else entity.link
        except AttributeError:
            entity.slug = None
            entity.real_link = entity.link

        if not hasattr(entity, 'image') or not entity.image:
            entity.is_default_image = True
            entity.image = settings.NEWS_FEED_DEFAULT_IMAGE

    return entries


def get_news_feeds():
    feed = feedparser.parse(settings.NEWS_FEED_URL)
    return feed.entries
