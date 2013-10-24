import linkType


class Link(object):
    """Represents a link to a resource"""

    def __init__(self, url, type=linkType.LinkType.ANCHOR):
        self.url = url
        self.type = type
