import http.client
import responseProcessor
import unittest
from unittest.mock import MagicMock


class ResponseProcessor_ProcessResponseTests(unittest.TestCase):
    def test_SetsResponseStatusCodeAndResponseDataAndLocationheader(self):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = { "Location": "the location" }
        sut = responseProcessor.ResponseProcessor()
        sut._read_response = MagicMock(return_value="response data")
        expected = "response data", 200, "the location"

        actual = sut.process_response(mock_response, True)

        self.assertEqual(expected, actual)

    def test_SetsResponseToNoneAndStatusCodeToTimeoutIfNoResponse(self):
        sut = responseProcessor.ResponseProcessor()

        data, status_code, _ = sut.process_response(None, True)

        self.assertEqual(None, data)
        self.assertEqual(http.client.GATEWAY_TIMEOUT, status_code)

if __name__ == '__main__':
    unittest.main()
