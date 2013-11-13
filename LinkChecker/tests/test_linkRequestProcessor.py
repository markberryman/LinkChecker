from linkrequest import linkRequestResult
from linkrequest import linkRequestProcessor
import unittest
from unittest.mock import MagicMock


class ResourceGetter_GetResourceTests(unittest.TestCase):
    def test_RaisesTypeErrorIflinkToProcessIsNone(self):
        sut = linkRequestProcessor.LinkRequestProcessor(None, None)

        self.assertRaises(TypeError, sut.process_link_request, None)

    def test_ReturnsLinkRequestResult(self):
        mock_link_request = MagicMock()
        mock_link_request.link_url = "link"
        mock_url_requester = MagicMock()
        mock_response_processor = MagicMock()
        mock_response_processor.process_response = MagicMock(return_value=("response", 200, "go here"))
        sut = linkRequestProcessor.LinkRequestProcessor(mock_url_requester, mock_response_processor)
        expected = linkRequestResult.LinkRequestResult(
            "link", 200, "response", "go here")
    
        actual = sut.process_link_request(mock_link_request)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
