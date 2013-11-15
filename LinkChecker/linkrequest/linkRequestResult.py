class LinkRequestResult(object):
    """Represents result of requesting a link."""
    def __init__(self, link_url, status_code, response, location_header):
        self.__link_url = link_url
        self.__status_code = status_code
        self.__response = response
        self._location_header = location_header

    def equals(self, other):
        return ((self.link_url == other.link_url) and
                (self.status_code == other.status_code) and
                (self.response == other.response))

    @property
    def link_url(self):
        return self.__link_url

    @property
    def response(self):
        return self.__response

    @property
    def status_code(self):
        return self.__status_code

    @property
    def location_header(self):
        return self._location_header
