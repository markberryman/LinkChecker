class LinkProcessor(object):
    """Processes the result of a link request. This involves 
    processing the markup for links, applying transforms and filters."""
    def __init__(
            self, linkFilterProcessor,
            linkTransformProcessor, html_link_parser):
        self.linkFilterProcessor = linkFilterProcessor
        self.linkTransformProcessor = linkTransformProcessor
        self._html_link_parser = html_link_parser

    def process_link(self, link_request_result):
        """Parses the link's response and then applies filters
        and transformers before returning the set of new links."""
        if (link_request_result is None):
            raise TypeError("link_request_result can not be None.")

        links_from_markup = self._html_link_parser.parse_markup(
            link_request_result.response)

        # apply transforms ahead of filtering b/c of the interaction
        # b/w the transform converting relative links to absolute links and the
        # filter which checks to ensure we're not leaving the root domain
        if (self.linkTransformProcessor is not None):
            processing_context = {
                "current_link_url": link_request_result.link_url
            }
            self.linkTransformProcessor.apply_transformers(
                processing_context, links_from_markup)

        if (self.linkFilterProcessor is not None):
            links_from_markup = self.linkFilterProcessor.apply_filters(links_from_markup)

        return links_from_markup
