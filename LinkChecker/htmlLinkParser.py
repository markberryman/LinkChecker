from link import link
from link import linkType
from html.parser import HTMLParser


class HTMLLinkParser(HTMLParser):
    """Parses HTML markup and returns the links."""
    def __init__(self):
        super().__init__(self)
        self._processing_functions = { 
            "a": self._process_anchor_tag,
            "link": self._process_link_tag,
            "script": self._process_script_tag,
            "img": self._process_image_tag
            }

    def find_links(self, markup):
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

        if (tag in self._processing_functions):
            newLink = self._processing_functions[tag](attrDict)

            # handling tags that don't have a link (i.e., bad markup)
            if (newLink is not None):
                self.links.add(newLink)

    @staticmethod
    def _process_anchor_tag(attrDict):
        if "href" in attrDict:
            return link.Link(attrDict["href"], linkType.LinkType.ANCHOR)

    @staticmethod
    def _process_link_tag(attrDict):
        if "rel" in attrDict:
            if (attrDict["rel"] == "stylesheet"):
                if "href" in attrDict:
                    return link.Link(
                        attrDict["href"], linkType.LinkType.STYLESHEET)

    @staticmethod
    def _process_script_tag(attrDict):
        if "src" in attrDict:
            return link.Link(attrDict["src"], linkType.LinkType.SCRIPT)

    @staticmethod
    def _process_image_tag(attrDict):
        if "src" in attrDict:
            return link.Link(attrDict["src"], linkType.LinkType.IMAGE)
