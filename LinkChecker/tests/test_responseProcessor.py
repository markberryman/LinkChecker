import http.client
from link import link, linkType
import responseProcessor
import unittest
from unittest.mock import MagicMock


class ResponseProcessor_ProcessResponseTests(unittest.TestCase):
    def test_ReturnsLinksFoundInMarkup(self):
        links = set()
        mock_html_link_parser = MagicMock()
        mock_html_link_parser.find_links = MagicMock(return_value=links)
        sut = responseProcessor.ResponseProcessor(None, None)
        sut._process_markup = MagicMock(return_value=links)
        expected = links

        actual = sut.process_response(None, None, None, None)

        self.assertEqual(expected, actual)

    def test_ReturnsLinkAssociatedWith302(self):
        dummy_location_header = "link"
        sut = responseProcessor.ResponseProcessor(None, None)
        expected = link.Link(dummy_location_header, linkType.LinkType.MOVED)

        actual = sut.process_response(None, None, http.client.FOUND, dummy_location_header).pop()

        # todo - use Link equality
        self.assertEqual(expected.url, actual.url)
        self.assertEqual(expected.type, actual.type)

    def test_InvokesPostProcessor(self):
        dummy_link = "link"
        dummy_processing_context = {
            "current_link_url": dummy_link
        }
        dummy_links_from_markup = set()
        mock_links_post_processor = MagicMock()
        mock_links_post_processor.apply_transforms_and_filters = MagicMock()
        sut = responseProcessor.ResponseProcessor(None, mock_links_post_processor)
        sut._process_markup = MagicMock(return_value=dummy_links_from_markup)

        sut.process_response(None, dummy_link, None, None)

        mock_links_post_processor.apply_transforms_and_filters.assert_called_with(
            dummy_links_from_markup, dummy_processing_context)

    def test_ReturnsLinksFromPostProcessor(self):
        links = set()
        mock_links_post_processor = MagicMock()
        mock_links_post_processor.apply_transforms_and_filters = MagicMock(return_value=links)
        sut = responseProcessor.ResponseProcessor(None, mock_links_post_processor)
        sut._process_markup = MagicMock()
        expected = links

        actual = sut.process_response(None, None, None, None)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
