import link
import linkType
from html.parser import HTMLParser


class HTMLLinkParser(HTMLParser):
    """Parses HTML markup and returns the number of discovered
    links."""
    def __init__(self):
        super().__init__(self)

    def parse_markup(self, markup):
        self.links = set()

        if (markup is None):
            return

        # toss all unprocessed data; needed b/c the parser
        # might have handled an invalid markup case and
        # there could be turd data left around to crunch
        self.reset()

        self.feed(markup)

        return self.links

    # tag and attribute values are automatically lowercased
    def handle_starttag(self, tag, attrs):
        newLink = None
        attrDict = dict(attrs)

        if (tag == "a"):
            newLink = self.__process_anchor_tag(attrDict)

        if (tag == "link"):
            newLink = self.__process_link_tag(attrDict)

        if (tag == "script"):
            newLink = self.__process_script_tag(attrDict)

        if (tag == "img"):
            newLink = self.__process_image_tag(attrDict)

        # handling tags that don't have a link (i.e., bad markup)
        if (newLink is not None):
            self.links.add(newLink)

    @staticmethod
    def __process_anchor_tag(attrDict):
        if "href" in attrDict:
            return link.Link(attrDict["href"], linkType.LinkType.ANCHOR)

    @staticmethod
    def __process_link_tag(attrDict):
        if "rel" in attrDict:
            if (attrDict["rel"] == "stylesheet"):
                if "href" in attrDict:
                    return link.Link(
                        attrDict["href"], linkType.LinkType.STYLESHEET)

    @staticmethod
    def __process_script_tag(attrDict):
        if "src" in attrDict:
            return link.Link(attrDict["src"], linkType.LinkType.SCRIPT)

    @staticmethod
    def __process_image_tag(attrDict):
        if "src" in attrDict:
            return link.Link(attrDict["src"], linkType.LinkType.IMAGE)
