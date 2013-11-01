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

    def __is_top_level_and_first_subdomain_equal(self, link):
        result = True

        linkHostnameSegments = urlparse(link).hostname.split(".")
        baseHostnameSegments = self.baseHostname.split(".")

        if ((linkHostnameSegments[len(linkHostnameSegments) - 1] ==
                baseHostnameSegments[len(baseHostnameSegments) - 1]) and
            (linkHostnameSegments[len(linkHostnameSegments) - 2] ==
                baseHostnameSegments[len(baseHostnameSegments) - 2])):
            result = False

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
                result = self.__is_top_level_and_first_subdomain_equal(link)

        return result
