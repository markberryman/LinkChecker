import http.client
import linkRequestResult
import socket


class ResourceGetter:
    def __init__(self, url_requester):
        self.url_requester = url_requester

    def make_request(self, url):
        result = None

        try:
            result = self.url_requester.request_url(url)
        except socket.error as msg:
            print("Socket error making request: {}".format(msg))

        return result

    def read_response(self, response):
        result = None

        try:
            result = response.read().decode()
        except UnicodeDecodeError:
            # going to hit this when response data includes binary
            # content (e.g. pdf file); instead of trying to filter
            # out all of these extensions, just swallow the exception
            # and move on for now
            pass

        return result

    def get_resource(self, link_request):
        """Process the link request object."""
        if (link_request is None):
            raise TypeError("link_request can not be None.")

        result_status_code = None
        response_data = None
        url = link_request.link_url

        response = self.make_request(url)

        if (response is not None):
            result_status_code = response.status

            if (link_request.read_response):
                response_data = self.read_response(response)
        else:
            # something went wrong w/ the request
            result_status_code = http.client.GATEWAY_TIMEOUT

        return linkRequestResult.LinkRequestResult(
            url, result_status_code, response_data)
