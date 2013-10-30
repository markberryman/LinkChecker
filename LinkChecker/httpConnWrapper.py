import http.client


class HttpConnWrapper(object):
    """Creates HTTP connections."""
    def create_connection(self, url_parts, timeout):
        return http.client.HTTPConnection(
            url_parts.netloc, None, None, timeout)
