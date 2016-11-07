from django.utils.safestring import mark_safe
from ttp import ttp

TWEET_PARSER = ttp.Parser()

def render_tweet_html(status):
    text = status.text
    try:
        return mark_safe(TWEET_PARSER.parse(text).html)
    except:  # better return something :(
        return text
