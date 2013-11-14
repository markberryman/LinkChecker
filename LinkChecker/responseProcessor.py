class ResponseProcessor(object):
    """Processes response data to find new links."""

    def __init__(
            self, html_link_parser,
            links_post_processor):
        self._html_link_parser = html_link_parser
        self._links_post_processor = links_post_processor

    def process_link(self, link_request_result):
        """Parses markup for new links, applies filters and transformers 
        and then returns set of new links."""
        if (link_request_result is None):
            raise TypeError("link_request_result can not be None.")

        # todo - rename "parse_markup" method to "get_links_from_markup"
        links_from_markup = self._html_link_parser.parse_markup(
            link_request_result.response)

        # todo - consider having this passed in?
        processing_context = {
            "current_link_url": link_request_result.link_url
        }

        if (self._links_post_processor is not None):
            links_from_markup = self._links_post_processor.apply_transforms_and_filters(
                links_from_markup, processing_context)

        return links_from_markup
