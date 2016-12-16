import tweepy
from django import template
from django.conf import settings

from digi.tweet_utils import render_tweet_html
from digi.utils import get_cached_with_mtime

TWEET_CACHE_REFRESH_AGE = 60 * 15  # if tweets are 15 minutes old, attempt reload

register = template.Library()


def get_tweepy_api():
    try:
        auth = tweepy.OAuthHandler(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
        )
        auth.set_access_token(
            key=settings.TWITTER_ACCESS_TOKEN,
            secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
        )
    except AttributeError:
        print('No Twitter tokens found in settings')
        return None
    return tweepy.API(auth)


@register.simple_tag()
def twitter_search(query):
    """
    Search Twitter for the given query and result results
    :param query:
    :type query:
    :return:
    :rtype:
    """
    tweepy_api = get_tweepy_api()
    if not tweepy_api:
        return None
    try:
        results = list(get_cached_with_mtime(
            cache_key='twitter_%s' % query,
            max_mtime=TWEET_CACHE_REFRESH_AGE,
            getter=lambda: tweepy_api.search(q=query, rpp=100, result_type='recent'),
            default=[],
        ))
    except tweepy.TweepError as error:
        print('Tweepy responded with error: ' + str(error))
        return None
    for result in results:
        result.html = render_tweet_html(result)
    return results
