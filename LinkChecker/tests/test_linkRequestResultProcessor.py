import http.client
import linkRequestResultProcessor
from unittest.mock import MagicMock
import unittest


class LinkRequestResultProcessor_ProcessLinkRequestResultTests(unittest.TestCase):
    def test_ReturnsBrokenLinks(self):
        mock_link_request_result = MagicMock()
        mock_link_request_result.link_url = "url"
        mock_link_request_result.status_code = http.client.NOT_FOUND
        mock_link_request_results = [mock_link_request_result]
        sut = linkRequestResultProcessor.LinkRequestResultProcessor(None)
        expected = ("url", http.client.NOT_FOUND)

        good_links, invalid_markup_links, broken_links = sut.process_link_request_result(mock_link_request_results)
        actual = broken_links.pop()

        self.assertEqual(actual[0], expected[0])
        self.assertEqual(actual[1], expected[1])


if __name__ == '__main__':
    unittest.main()
