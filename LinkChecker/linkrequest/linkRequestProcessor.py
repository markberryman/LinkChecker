import http.client
from . import linkRequestResult


class LinkRequestProcessor:
    """Processes LinkRequest objects."""
    def __init__(self, url_requester, response_processor):
        self._url_requester = url_requester
        self._response_processor = response_processor

    def _make_request_and_process_response(self, url, read_response):
        # todo - also get the response headers
        response = self._url_requester.request_url(url)
        
        response_data, result_status_code = self._response_processor.process_response(
            response, read_response)

        return response_data, result_status_code

    def process_link_request(self, link_request):
        """Process LinkRequest and returns LinkRequestResult."""
        if (link_request is None):
            raise TypeError("link_request can not be None.")

        result_status_code = None
        response_data = None
        url = link_request.link_url

        response_data, result_status_code = self._make_request_and_process_response(
            url, link_request.read_response)

        print("[{}] {}\n  --> {}\n".format(result_status_code,
                                          http.client.responses[result_status_code].upper(),
                                          url))
        
        # todo - add response headers
        return linkRequestResult.LinkRequestResult(
            url, result_status_code, response_data)
