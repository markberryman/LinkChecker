import socket
from unittest.mock import MagicMock
import urlRequester
import unittest


class UrlRequester_RequestUrlTests(unittest.TestCase):
    def test_RaisesTypeErrorIfUrlIsNone(self):
        sut = urlRequester.UrlRequester(None, None)

        self.assertRaises(TypeError, sut.request_url, None)

    def test_CreatesHttpConnectionWithProvidedUrlAndTimeout(self):
        mock_url_parts = MagicMock()
        mock_url_parts.path = "path"
        mock_url_parse_wrapper = MagicMock()
        mock_url_parse_wrapper.parse_url = MagicMock(return_value=mock_url_parts)
        mock_http_conn_wrapper = MagicMock()
        dummy_url = "http://foo.com/path"
        sut = urlRequester.UrlRequester(
            mock_http_conn_wrapper, mock_url_parse_wrapper)

        sut.request_url(dummy_url)

        mock_http_conn_wrapper.create_connection.assert_called_with(
            mock_url_parts, 5)

    def test_MakesGetRequestWithuserAgentHeader(self):
        mock_url_parts = MagicMock()
        mock_url_parts.path = "path"
        mock_url_parse_wrapper = MagicMock()
        mock_url_parse_wrapper.parse_url = MagicMock(return_value=mock_url_parts)
        mock_http_conn = MagicMock()
        mock_http_conn_wrapper = MagicMock()
        mock_http_conn_wrapper.create_connection = MagicMock(return_value=mock_http_conn)
        sut = urlRequester.UrlRequester(
            mock_http_conn_wrapper, mock_url_parse_wrapper)

        sut.request_url("some url")

        mock_http_conn.request.assert_called_with(
            "GET", mock_url_parts.path, body=None, headers={ "User-Agent": "linkChecker" })
        
    def test_HandlesSocketErrorWhenGettingResponse(self):
        mock_url_parts = MagicMock()
        mock_url_parts.path = "path"
        mock_url_parse_wrapper = MagicMock()
        mock_url_parse_wrapper.parse_url = MagicMock(return_value=mock_url_parts)
        mock_http_conn = MagicMock()
        mock_http_conn.getresponse = MagicMock(side_effect=socket.error)
        mock_http_conn_wrapper = MagicMock()
        mock_http_conn_wrapper.create_connection = MagicMock(return_value=mock_http_conn)
        sut = urlRequester.UrlRequester(
            mock_http_conn_wrapper, mock_url_parse_wrapper)
        expected = None

        actual = sut.request_url("some url")

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
