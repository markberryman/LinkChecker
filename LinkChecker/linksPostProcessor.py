class LinksPostProcessor(object):
    """Applies transforms and filters to a set of links."""
    def __init__(self, linkFilterProcessor, linkTransformProcessor):
        self.linkFilterProcessor = linkFilterProcessor
        self.linkTransformProcessor = linkTransformProcessor

    def apply_transforms_and_filters(self, links, processing_context):
        # apply transforms ahead of filtering b/c of the interaction
        # b/w the transform converting relative links to absolute links and the
        # filter which checks to ensure we're not leaving the root domain
        if (self.linkTransformProcessor is not None):
            self.linkTransformProcessor.apply_transformers(
                processing_context, links)

        if (self.linkFilterProcessor is not None):
            links = self.linkFilterProcessor.apply_filters(links)

        return links
