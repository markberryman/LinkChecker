import http.client
from link import link, linkType


class ResponseProcessor(object):
    """Processes response to find new links."""

    def __init__(
            self, html_link_parser,
            links_post_processor):
        self._html_link_parser = html_link_parser
        self._links_post_processor = links_post_processor

    # not inlining this method yet since it makes unit testing a bit easier
    def _process_302_response(self, location_header):
        # todo - consider creating a new link type?
        return link.Link(location_header, linkType.LinkType.ANCHOR)

    def process_response(self, markup, link_url, status_code, location_header):
        """Returns links found in markup and returns link corresponding to
        new location associated with a 302 response."""
        links = set()
        
        if (self._html_link_parser is not None):
            links_from_markup = self._html_link_parser.find_links(markup)

            if (links_from_markup is not None):
                links = links.union(links_from_markup)

        if (status_code == http.client.FOUND):
            links.add(self._process_302_response(location_header))

        # todo - consider having this passed in?
        # todo - just pass the link_url directly rather than a context; YAGNI
        processing_context = {
            "current_link_url": link_url
        }

        if (self._links_post_processor is not None):
            # todo - why is a links value returned here instead of in-place
            # modification?
            links = self._links_post_processor.apply_transforms_and_filters(
                links, processing_context)

        return links
