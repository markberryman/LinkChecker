from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse


class LinkTransform(object):
    """Parent class for defining link transforms."""

    def transform(self, processing_context, link):
        if (processing_context is None):
            raise TypeError("processing_context can not be None.")

        if (link is None):
            raise TypeError("link can not be None.")


class LowerCaseTransform(LinkTransform):
    """Lower cases parts of url that don't alter semantics.
    Don't touch anything beyond the domain name."""
    def transform(self, context, newLink):
        urlparts = urlparse(newLink.url)
        # have to explicitly create a tuple to pass to urlunparse
        # b/c we can't modify the values on the urlparts obj directly
        newLink.url = urlunparse(
            (urlparts.scheme.lower(), urlparts.netloc.lower(),
             urlparts.path, urlparts.params,
             urlparts.query, urlparts.fragment))


class RelativeLinkTransform(LinkTransform):
    """Transforms relative links to absolute links."""
    def transform(self, processing_context, link):
        super(RelativeLinkTransform, self).transform(processing_context, link)             

        current_link_url = processing_context["current_link_url"]

        link.url = urljoin(current_link_url, link.url)
