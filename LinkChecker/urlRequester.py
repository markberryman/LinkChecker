import socket


class UrlRequester(object):
    """Requests a url."""
    def __init__(self, http_conn_wrapper, url_parse_wrapper):
        # timeout in seconds
        self.connTimeout = 5
        self._http_conn_wrapper = http_conn_wrapper
        self._url_parse_wrapper = url_parse_wrapper

    def _make_request(self, urlParts):
        # need to include some user agent value otherwise
        # sites are rejecting the request
        headers = {"User-Agent": "linkChecker"}
        
        conn = self._http_conn_wrapper.create_connection(urlParts, self.connTimeout)
        
        conn.request("GET", urlParts.path, body=None, headers=headers)

        return conn

    def request_url(self, url):
        """Requests a url and returns an HTTPResponse object."""
        result = None

        if (url is None):
            raise TypeError("URL can not be none.")

        urlParts = self._url_parse_wrapper.parse_url(url)
                
        conn = self._make_request(urlParts)

        try:
            # todo - get response headers
            result = conn.getresponse()
        except socket.error as msg:
            print("Socket error making request: {}".format(msg))
        
        return result
