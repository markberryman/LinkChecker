class LinkTransformProcessor(object):
    """Transforms links based on a supplied set of transformers."""

    def __init__(self, transformers):
        self.transformers = transformers

    def apply_transformers(self, processing_context, links):
        """Applies transformers to links. The provided
        processing_context contains add'l info required by some transforms."""
        if (processing_context is None):
            raise TypeError("processing_context can not be None.")

        if (links is None):
            raise TypeError("links can not be None.")

        for transformer in self.transformers:
            [transformer.transform(processing_context, link) for link in links]
