from wagtail.wagtailcore import hooks


def allow_blindly(tag):
    return tag

# See: http://docs.wagtail.io/en/v1.6/reference/hooks.html#construct-whitelister-element-rules
@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    rules = {}
    # Tables
    rules.update(dict.fromkeys(['table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td'], allow_blindly))
    # Divs, spans, code and anchors
    rules.update(dict.fromkeys(['div', 'span', 'a', 'code', 'pre', 'blockquote', 'section'], allow_blindly))
    return rules
