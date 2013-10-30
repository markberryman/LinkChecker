import http.client


class ResponseProcessor(object):
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
        """Examines response and returns appropriate
        status code and response data if desired."""
        response_data = None
        result_status_code = None

        if (response is not None):
            result_status_code = response.status
        
            if (read_response):
                response_data = self._read_response(response)
        else:
            # something went wrong w/ the request
            result_status_code = http.client.GATEWAY_TIMEOUT

        return response_data, result_status_code
