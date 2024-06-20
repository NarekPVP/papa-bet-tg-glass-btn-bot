import re


def is_valid_url(url):
    url_regex = re.compile(r'https?://(?:www\.)?[a-zA-Z0-9./]+')
    return bool(url_regex.match(url))
