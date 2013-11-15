import html.parser
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

        self.assertEqual(expected[0], actual[0])
        self.assertEqual(expected[1], actual[1])

    def test_ReturnsInvalidMarkupLinks(self):
        mock_link_request_result = MagicMock()
        mock_link_request_result.link_url = "url"
        mock_link_request_results = [mock_link_request_result]
        mock_response_processor = MagicMock()
        mock_response_processor.process_response = MagicMock(side_effect=html.parser.HTMLParseError("error"))
        sut = linkRequestResultProcessor.LinkRequestResultProcessor(mock_response_processor)
        sut._is_link_broken = MagicMock(return_value=False)
        expected = "url"

        good_links, invalid_markup_links, broken_links = sut.process_link_request_result(mock_link_request_results)
        actual = invalid_markup_links.pop()

        self.assertEqual(expected, actual)
    
    def test_ReturnsUniqueGoodLinksLinks(self):
        dummy_links = ["link1", "link2", "link1"]
        mock_link_request_result = MagicMock()
        mock_link_request_results = [mock_link_request_result]
        mock_response_processor = MagicMock()
        mock_response_processor.process_response = MagicMock(return_value=dummy_links)
        sut = linkRequestResultProcessor.LinkRequestResultProcessor(mock_response_processor)
        sut._is_link_broken = MagicMock(return_value=False)
        expected = set().union(set(dummy_links))

        good_links, invalid_markup_links, broken_links = sut.process_link_request_result(mock_link_request_results)
        actual = good_links

        self.assertEqual(expected, actual)
            

if __name__ == '__main__':
    unittest.main()
