import http.client
import link
import linkRequestResult
import socket


class ResourceGetter:
    def __init__(self, content_requester):
        self.content_requester = content_requester

    def get_resource(self, link_request):
        """Process the link request object."""
        if (link_request is None):
            raise TypeError("link_request can not be None.")

        result_status_code = None
        response_data = None
        url = link_request.link_url

        try:
            res = self.content_requester.request_url(url)

            result_status_code = res.status

            if (link_request.read_response):
                try:
                    response_data = res.read().decode()
                except UnicodeDecodeError:
                    # going to hit this when response data includes binary
                    # content (e.g. pdf file); instead of trying to filter
                    # out all of these extensions, just swallow the exception
                    # and move on for now
                    pass
        except socket.error as msg:
            # not decoding the msg error code value to a meaningful
            # http status code; since we're primarily hitting timeouts
            # we'll go w/ that
            print("Socket error making request: {}".format(msg))
            result_status_code = http.client.GATEWAY_TIMEOUT

        return linkRequestResult.LinkRequestResult(
            url, result_status_code, response_data)
