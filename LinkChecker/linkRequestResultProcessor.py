import http.client
import html.parser


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
            if (LinkRequestResultProcessor._is_link_broken(link_request_result.status_code) is False):
                if (link_request_result.response is not None):
                    try:
                        good_links = good_links.union(
                            set(self._link_processor.process_link(link_request_result)))
                    except html.parser.HTMLParseError:
                        invalid_markup_links.add(link_request_result.link_url)
            else:
                broken_links.add(
                    (link_request_result.link_url, link_request_result.status_code))

        return good_links, invalid_markup_links, broken_links

    @staticmethod
    def _is_link_broken(status_code):
        return ((status_code < http.client.OK) or
                (status_code >= http.client.BAD_REQUEST))
