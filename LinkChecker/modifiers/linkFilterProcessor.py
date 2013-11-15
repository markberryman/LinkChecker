class LinkFilterProcessor(object):
    """Filters links based on a supplied set of filters."""

    def __init__(self, filters):
        self.filters = filters

    def apply_filters(self, links):
        """Applies filters to links."""
        if (links is not None):
            for filter in self.filters:
                linksToFilter = set(
                    [link for link in links if filter.should_filter(link.url)])
                links = links.difference(linksToFilter)

        return links
