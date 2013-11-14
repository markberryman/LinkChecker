import http.client


class ResponseBuilder(object):
    """Breaks down a web response into component parts."""

    def _read_response(self, response):
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

    def process_response(self, response, read_response):
        """Breaks down response and returns status code, select response 
        headers and data if requested."""
        response_data = None
        location_header = None
        result_status_code = None

        if (response is not None):
            result_status_code = response.status
            # only getting the Location header b/c we use it to handle 302 responses
            location_header = response.headers["Location"]
        
            if (read_response):
                response_data = self._read_response(response)
        else:
            # something went wrong w/ the request
            result_status_code = http.client.GATEWAY_TIMEOUT

        return response_data, result_status_code, location_header
