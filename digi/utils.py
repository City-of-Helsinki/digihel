import logging
import time

from django.conf import settings
from django.core.cache import cache

log = logging.getLogger(__name__)


def get_cached_with_mtime(cache_key, getter, max_mtime=60, default=None, expiry=86400):
    """
    Get something with a maximum modification time.

    I.e. if the data stored in the cache is older than max_mtime seconds (or does not
    exist), it attempts to call getter() for a new value.

    However, if the

    :param cache_key: Cache key string
    :type cache_key: str
    :param getter: Getter function
    :type getter: function
    :param max_mtime: Maximum modification time, in seconds
    :type max_mtime: int
    :param default: Default value, if nothing is in the cache
    :type default: object
    :param expiry: Maximum expiry for the cache entity, in seconds
    :type expiry: int
    :return: data, from the getter or the cache
    :rtype: object
    """
    cached_data = cache.get(cache_key)
    if cached_data is None or (time.time() - cached_data['mtime']) > max_mtime:
        try:
            cached_data = {
                'mtime': time.time(),
                'data': getter(),
            }
            cache.set(cache_key, cached_data, expiry)
        except Exception:
            if settings.DEBUG:
                raise
            log.warn('error fetching in get_cached_with_mtime(%s)', cache_key, exc_info=True)
            if cached_data is None:
                # If we didn't have anything cached to begin with,
                # at least cache something for a while to avoid hammering the original `getter()`
                cached_data = {'mtime': time.time(), 'data': default}
                cache.set(cache_key, cached_data, max_mtime)
    return cached_data['data']
