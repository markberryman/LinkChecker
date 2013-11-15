from . import linkType


class Link(object):
    """Represents a link to a resource"""

    def __init__(self, url, type=linkType.LinkType.ANCHOR):
        self.url = url
        self.type = type

    def equals(self, other):
        return ((self.url == other.url) and
                (self.type == other.type))
