import http.client
import linkRequestResult
import resourceGetter
import unittest
from unittest.mock import MagicMock


class ResourceGetter_GetResourceTests(unittest.TestCase):
    def test_RaisesTypeErrorIflinkToProcessIsNone(self):
        sut = resourceGetter.ResourceGetter(None)

        self.assertRaises(TypeError, sut.process_link_request, None)

    def test_SetsResponseStatusCodeAndResponseData(self):
        mock_link_request = MagicMock()
        mock_link_request.link_url = "link"
        mock_link_request.read_response = True

        mock_response = MagicMock()
        mock_response.status = 200

        mock_url_requester = MagicMock()
        mock_url_requester.request_url = MagicMock(return_value=mock_response)

        sut = resourceGetter.ResourceGetter(mock_url_requester)
        sut._read_response = MagicMock(return_value="response data")
        expected = linkRequestResult.LinkRequestResult("link", 200, "response data")

        actual = sut.process_link_request(mock_link_request)

        self.assertEqual(expected, actual)

    def test_SetsResponseToNoneAndStatusCodeToTimeoutIfNoResponse(self):
        mock_url_requester = MagicMock()
        mock_url_requester.request_url = MagicMock(return_value=None)

        mock_link_request = MagicMock()
        mock_link_request.link_url = "link"

        sut = resourceGetter.ResourceGetter(mock_url_requester)
        sut.make_request = MagicMock(return_value=None)
        expected = linkRequestResult.LinkRequestResult(
            "link", http.client.GATEWAY_TIMEOUT, None)

        actual = sut.process_link_request(mock_link_request)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
