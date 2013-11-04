from linkrequest import linkRequestResult
from linkrequest import linkRequestProcessor
import unittest
from unittest.mock import MagicMock


class ResourceGetter_GetResourceTests(unittest.TestCase):
    def test_RaisesTypeErrorIflinkToProcessIsNone(self):
        sut = linkRequestProcessor.LinkRequestProcessor(None, None)

        self.assertRaises(TypeError, sut.process_link_request, None)

    def test_CallsMakeRequestAndProcessResponse(self):
        mock_link_request = MagicMock()
        sut = linkRequestProcessor.LinkRequestProcessor(None, None)
        sut._make_request_and_process_response = MagicMock(return_value=("response", 200))
    
        sut.process_link_request(mock_link_request)

        sut._make_request_and_process_response.assert_called_with(
            mock_link_request.link_url, mock_link_request.read_response)

    def test_ReturnsLinkRequestResult(self):
        mock_link_request = MagicMock()
        mock_link_request.link_url = "link"
        sut = linkRequestProcessor.LinkRequestProcessor(None, None)
        sut._make_request_and_process_response = MagicMock(return_value=("response", 200))
        expected = linkRequestResult.LinkRequestResult(
            "link", 200, "response")
    
        actual = sut.process_link_request(mock_link_request)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
