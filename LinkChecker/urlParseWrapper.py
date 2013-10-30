from urllib.parse import urlparse


class UrlParseWrapper(object):
    """Parses a url into pieces."""
    def parse_url(self, url):
        return urlparse(url)
