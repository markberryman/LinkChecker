class LinkRequest(object):
    """Represents a unit of work for requesting a link with
    additional metadata controlling handling the request."""
    def __init__(self, link_url, read_response):
        self.__link_url = link_url
        self.__read_response = read_response

    @property
    def link_url(self):
        return self.__link_url

    @property
    def read_response(self):
        return self.__read_response
