import http.client
from link import link, linkType


class ResponseProcessor(object):
    """Processes response to find new links."""

    def __init__(
            self, html_link_parser,
            links_post_processor):
        self._html_link_parser = html_link_parser
        self._links_post_processor = links_post_processor

    def _process_markup(self, markup):
        """Parses markup for new links and returns set of new links."""

        # todo - inline this method?

        # todo - rename "parse_markup" method to "get_links_from_markup"
        return self._html_link_parser.parse_markup(markup)

    # todo - inline this method?
    def _process_302_response(self, location_header):
        return link.Link(location_header, linkType.LinkType.ANCHOR)

    # todo - add unit tests
    def process_response(self, markup, link_url, status_code, location_header):
        """Returns links found in markup and returns link corresponding to
        new location associated with a 302 response."""
        links = set()
        
        links_from_markup = self._process_markup(markup)

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
