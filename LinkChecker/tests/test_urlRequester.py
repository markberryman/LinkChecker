import socket
from unittest.mock import MagicMock
import urlRequester
import unittest


class UrlRequester_RequestUrlTests(unittest.TestCase):
    def test_RaisesTypeErrorIfUrlIsNone(self):
        sut = urlRequester.UrlRequester(None, None)

        self.assertRaises(TypeError, sut.request_url, None)

    def test_CreatesHttpConnectionWithProvidedUrl(self):
        dummy_url_parts = "url parts"
        mock_url_parse_wrapper = MagicMock()
        mock_url_parse_wrapper.parse_url = MagicMock(return_value=dummy_url_parts)
        sut = urlRequester.UrlRequester(None, mock_url_parse_wrapper)
        sut._make_request = MagicMock()

        sut.request_url("url")

        sut._make_request.assert_called_with(dummy_url_parts)

    # todo - should really test that we print/log something here
    def test_HandlesSocketErrorWhenGettingResponse(self):
        mock_http_conn = MagicMock()
        mock_http_conn.getresponse = MagicMock(side_effect=socket.error)
        sut = urlRequester.UrlRequester(
            None, None)
        sut._url_parse_wrapper = MagicMock()
        sut._make_request = MagicMock(return_value=mock_http_conn)
        expected = None

        actual = sut.request_url("some url")

        self.assertEqual(expected, actual)
            
    def test_ReturnsResponse(self):
        dummy_response = "response"
        mock_http_conn = MagicMock()
        mock_http_conn.getresponse = MagicMock(return_value=dummy_response)
        sut = urlRequester.UrlRequester(
            None, None)
        sut._url_parse_wrapper = MagicMock()
        sut._make_request = MagicMock(return_value=mock_http_conn)
        expected = dummy_response

        actual = sut.request_url("some url")

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
