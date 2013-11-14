import http.client
import html.parser
from link import link, linkType


class LinkRequestResultProcessor(object):
    """Processes LinkRequestResult objects."""

    def __init__(self, link_processor):
        self._link_processor = link_processor

    def process_link_request_result(self, link_request_results):
        """Process list of LinkRequestResult objects and return
        good, invalid markup and broken links."""

        good_links = set()
        invalid_markup_links = set()
        broken_links = set()

        for link_request_result in link_request_results:
            new_links = set()

            if (self._is_link_broken(link_request_result.status_code) is False):
                if (link_request_result.status_code == http.client.FOUND):
                    # 302 status code
                    # todo - bit of a hack here
                    # todo - problem when the location header is a relative link
                    # todo - leads to possibility of applying transforms/modifiers at this point
                    found_link = link.Link(link_request_result.location_header, linkType.LinkType.ANCHOR)
                    new_links.add(found_link)
                else:
                    if (link_request_result.response is not None):
                        try:
                            new_links = set(self._link_processor.process_link(link_request_result))
                        except html.parser.HTMLParseError:
                            invalid_markup_links.add(link_request_result.link_url)
            else:
                broken_links.add(
                    (link_request_result.link_url, link_request_result.status_code))

            good_links = good_links.union(new_links)

        return good_links, invalid_markup_links, broken_links

    def _is_link_broken(self, status_code):
        return ((status_code < http.client.OK) or
                (status_code >= http.client.BAD_REQUEST))
