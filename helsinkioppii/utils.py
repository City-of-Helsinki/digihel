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


def get_substrings(string, delimiter=';', strip=True):
    """
    Returns a list of substrings extracted from given string that are
    separated by given delimiter.

    :param string: String from which the substrings are looked up from.
    :param delimiter: Character (sequence) that break up multiple substrings.
    :param strip: Flag for stripping leading and trailing whitespace from the
                  substring.
    :return: List of substrings
    """
    substrings = []
    for substring in string.split(delimiter):
        if strip:
            substring = substring.strip()
        substrings.append(substring)
    return substrings


def humanized_range(start, stop, step=1):
    """
    Return range from start to stop where stop is the last value of the range.

    >>> [i for i in range(1, 5)] == [1, 2, 3, 4]
    True
    >>> [i for i in humanized_range(1, 5)] == [1, 2, 3, 4, 5]
    True

    :param start: Starting value of the range
    :param stop: Last value of the range
    :param step: Increment between values
    :return: range
    """
    return range(start, stop + 1, step)
