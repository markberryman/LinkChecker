class LinkProcessor(object):
    """Processes the result of making a request for a link. This involves 
    processing the markup to look for new links and then applying transforms 
    and filters to those links."""
    def __init__(
            self, linkFilterProcessor,
            linkTransformProcessor, html_link_parser):
        self.linkFilterProcessor = linkFilterProcessor
        self.linkTransformProcessor = linkTransformProcessor
        self._html_link_parser = html_link_parser

    def process_link(self, link_request_result):
        """Parses markup for new links, applies filters and transformers 
        and then returns set of new links."""
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
