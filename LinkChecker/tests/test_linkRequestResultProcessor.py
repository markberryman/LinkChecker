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

        self.assertEqual(actual[0], expected[0])
        self.assertEqual(actual[1], expected[1])

    def test_ReturnsInvalidMarkupLinks(self):
        mock_link_request_result = MagicMock()
        mock_link_request_result.link_url = "url"
        mock_link_request_result.status_code = http.client.OK
        mock_link_request_result.response = "response"
        mock_link_request_results = [mock_link_request_result]
        mock_link_processor = MagicMock()
        mock_link_processor.process_link = MagicMock(side_effect=html.parser.HTMLParseError("error"))
        sut = linkRequestResultProcessor.LinkRequestResultProcessor(mock_link_processor)
        expected = "url"

        good_links, invalid_markup_links, broken_links = sut.process_link_request_result(mock_link_request_results)
        actual = invalid_markup_links.pop()

        self.assertEqual(expected, actual)
    
    def test_ReturnsGoodLinksLinks(self):
        mock_link_request_result = MagicMock()
        mock_link_request_result.status_code = http.client.OK
        mock_link_request_result.response = "response"
        mock_link_request_results = [mock_link_request_result]
        mock_link_processor = MagicMock()
        mock_link_processor.process_link = MagicMock(return_value=["link1", "link2"])
        sut = linkRequestResultProcessor.LinkRequestResultProcessor(mock_link_processor)
        expected = set().union(set(["link1", "link2"]))

        good_links, invalid_markup_links, broken_links = sut.process_link_request_result(mock_link_request_results)
        actual = good_links

        self.assertEqual(expected, actual)
            

if __name__ == '__main__':
    unittest.main()
