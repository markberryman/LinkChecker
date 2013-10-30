import http.client
import responseProcessor
import unittest
from unittest.mock import MagicMock


class ResponseProcessor_ProcessResponseTests(unittest.TestCase):
    def test_SetsResponseStatusCodeAndResponseData(self):
        mock_response = MagicMock()
        mock_response.status = 200
        sut = responseProcessor.ResponseProcessor()
        sut._read_response = MagicMock(return_value="response data")
        expected = "response data", 200

        actual = sut.process_response(mock_response, True)

        self.assertEqual(expected, actual)

    def test_SetsResponseToNoneAndStatusCodeToTimeoutIfNoResponse(self):
        sut = responseProcessor.ResponseProcessor()
        expected = None, http.client.GATEWAY_TIMEOUT

        actual = sut.process_response(None, True)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
