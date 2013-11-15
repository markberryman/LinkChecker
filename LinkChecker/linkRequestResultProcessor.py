import http.client
import html.parser


class LinkRequestResultProcessor(object):
    """Processes LinkRequestResult objects."""

    def __init__(self, response_processor):
        self._response_processor = response_processor

    def process_link_request_result(self, link_request_results):
        """Process list of LinkRequestResult objects and return
        good, invalid markup and broken links."""

        good_links = set()
        invalid_markup_links = set()
        broken_links = set()

        for link_request_result in link_request_results:
            if (self._is_link_broken(link_request_result.status_code) is False):
                try:
                    new_links = self._response_processor.process_response(
                        link_request_result.response, link_request_result.link_url,
                        link_request_result.status_code,
                        link_request_result.location_header)

                    good_links = good_links.union(new_links)
                except html.parser.HTMLParseError:
                    invalid_markup_links.add(link_request_result.link_url)
            else:
                broken_links.add(
                    (link_request_result.link_url, link_request_result.status_code))

        return good_links, invalid_markup_links, broken_links

    def _is_link_broken(self, status_code):
        return ((status_code < http.client.OK) or
                (status_code >= http.client.BAD_REQUEST))
