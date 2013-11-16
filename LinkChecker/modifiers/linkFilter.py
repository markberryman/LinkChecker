from urllib.parse import urlparse


class LinkFilter(object):
    """Abstract class defining for filtering links."""
    def should_filter(self, dataItem):
        raise NotImplementedError()


class MailToFilter(LinkFilter):
    def should_filter(self, link):
        return link.lower().startswith("mailto:")


class DomainCheckFilter(LinkFilter):
    def __init__(self, baseLink):
        self.baseHostname = urlparse(baseLink).hostname

    def _is_top_level_and_first_subdomain_equal(self, link):
        result = True

        # want to compare the last and second to last hostname segment
        # reversing the strings to make the future comparison a bit simpler
        link_hostname_segments = urlparse(link).hostname[::-1].split(".")
        base_hostname_segments = self.baseHostname[::-1].split(".")

        result = (not 
                  ((link_hostname_segments[0] == base_hostname_segments[0]) and
                  (link_hostname_segments[1] == base_hostname_segments[1])))

        return result

    def should_filter(self, link):
        """Returns false if hostname of link equals hostname of
        baselink or if the top level domain and the first level
        of subdomain are equal."""
        result = True

        # handle the intranet case as well w/ this check
        if (urlparse(link).hostname == self.baseHostname):
            result = False
        else:
            if ((urlparse(link).hostname is not None) and
                    (self.baseHostname is not None)):
                result = self._is_top_level_and_first_subdomain_equal(link)

        return result
