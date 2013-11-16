class LinkRequest(object):
    """Represents a unit of work for requesting a link with
    additional metadata controlling handling the request."""
    def __init__(self, link_url, read_response):
        self.link_url = link_url
        self.read_response = read_response
