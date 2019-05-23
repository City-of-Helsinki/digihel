import re

import feedparser
from django.conf import settings


def get_news_feeds():
    img_re = re.compile(r'<img.*?src=["\']+(.*?)["\']+/>')
    feed_result = feedparser.parse(settings.NEWS_FEED_URL)
    for entity in feed_result.entries:
        img_search = img_re.search(entity.description)
        try:
            entity.image = img_search.group(1)
            entity.parsed_description = img_re.sub('', entity.description)
        except AttributeError:
            pass
        if not hasattr(entity, 'image') or not entity.image:
            entity.is_default_image = True
            entity.image = settings.NEWS_FEED_DEFAULT_IMAGE
    return feed_result.entries
