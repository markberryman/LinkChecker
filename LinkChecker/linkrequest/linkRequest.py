class LinkRequest(object):
    """Represents a unit of work for requesting a link with
    additional metadata controlling handling the request."""
    def __init__(self, link_url, read_response):
        self._link_url = link_url
        self._read_response = read_response

    @property
    def link_url(self):
        return self._link_url

    @property
    def read_response(self):
        return self._read_response
