class LinkRequestResult(object):
    """Represents result of requesting a link."""
    def __init__(self, link_url, status_code, response, location_header):
        self.link_url = link_url
        self.status_code = status_code
        self.response = response
        self.location_header = location_header

    def equals(self, other):
        return ((self.link_url == other.link_url) and
                (self.status_code == other.status_code) and
                (self.response == other.response))
