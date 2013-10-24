import http.client
from urllib.parse import urlparse


class UrlRequester(object):
    """Requests a url."""
    def __init__(self):
        # timeout in seconds
        self.connTimeout = 5

    def request_url(self, url):
        if (url is None):
            raise TypeError("URL can not be none.")

        urlParts = urlparse(url)

        # need to include some user agent value otherwise
        # sites are rejecting the request
        headers = {"User-Agent": "linkChecker"}

        conn = http.client.HTTPConnection(
            urlParts.netloc, None, None, self.connTimeout)

        conn.request("GET", urlParts.path, body=None, headers=headers)

        return conn.getresponse()
