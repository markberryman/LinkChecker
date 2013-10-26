import http.client
import linkRequestResult
import resourceGetter
import unittest
from unittest.mock import MagicMock


class ResourceGetter_GetResourceTests(unittest.TestCase):
    def test_RaisesTypeErrorIflinkToProcessIsNone(self):
        sut = resourceGetter.ResourceGetter(None)

        self.assertRaises(TypeError, sut.get_resource, None)

    def test_SetsResponseStatusCodeAndResponseDataForAnchorTag(self):
        mock_link_request = MagicMock()
        mock_link_request.link_url = "link"
        mock_link_request.read_response = True

        mock_response = MagicMock()
        mock_response.status = 200

        sut = resourceGetter.ResourceGetter(None)
        sut.make_request = MagicMock(return_value=mock_response)
        sut.read_response = MagicMock(return_value="response data")
        expected = linkRequestResult.LinkRequestResult("link", 200, "response data")

        actual = sut.get_resource(mock_link_request)

        self.assertEqual(expected, actual)

    def test_SetsResponseToNoneAndStatusCodeToTimeoutIfNoResponse(self):
        mock_link_request = MagicMock()
        mock_link_request.link_url = "link"

        sut = resourceGetter.ResourceGetter(None)
        sut.make_request = MagicMock(return_value=None)
        expected = linkRequestResult.LinkRequestResult(
            "link", http.client.GATEWAY_TIMEOUT, None)

        actual = sut.get_resource(mock_link_request)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
