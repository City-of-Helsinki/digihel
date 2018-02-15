import re


def strip_dangerous_html(html):
    """
    Strip dangerous html content from given string.
    """
    # Pattern that matches handlers like "onSubmit" etc.
    on_pattern = re.compile(r'(?i)\s?on\w+="[^"]+"\s?')
    # Pattern that matches script tags
    script_pattern = re.compile(r'(?i)<script[\s\S]+?/script>')
    # Pattern that matches iframe tags
    iframe_pattern = re.compile(r'(?i)<iframe[\s\S]+?/iframe>')

    html = re.sub(on_pattern, '', html)
    html = re.sub(script_pattern, '', html)
    return re.sub(iframe_pattern, '', html)
