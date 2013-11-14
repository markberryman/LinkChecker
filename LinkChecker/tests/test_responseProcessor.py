import responseProcessor
import unittest
from unittest.mock import MagicMock


class ResponseProcessor_ProcessMarkupTests(unittest.TestCase):
    def test_RaisesTypeErrorIfLinkRequestResultIsNone(self):
        sut = responseProcessor.ResponseProcessor(None, None)

        self.assertRaises(TypeError, sut.process_markup, None)

    def test_InvokesLinksPostProcessor(self):
        dummy_link_url = "url"
        mock_link_request_result = MagicMock()
        mock_link_request_result.link_url = dummy_link_url
        mock_html_link_parser = MagicMock()
        dummy_links_from_markup = "links"
        mock_html_link_parser.parse_markup = MagicMock(return_value=dummy_links_from_markup)
        dummy_processing_context = {
            "current_link_url": dummy_link_url
        }
        mock_links_post_processor = MagicMock()
        sut = responseProcessor.ResponseProcessor(
            mock_html_link_parser, mock_links_post_processor)

        sut.process_markup(mock_link_request_result)

        mock_links_post_processor.apply_transforms_and_filters.assert_called_with(
            dummy_links_from_markup, dummy_processing_context)
    
    def test_ReturnsLinksFromPostProcessor(self):
        mock_link_request_result = MagicMock()
        dummy_links_from_markup = "links"
        mock_links_post_processor = MagicMock()
        mock_links_post_processor.apply_transforms_and_filters = MagicMock(return_value=dummy_links_from_markup)
        mock_html_link_parser = MagicMock()
        sut = responseProcessor.ResponseProcessor(
            mock_html_link_parser, mock_links_post_processor)
        expected = dummy_links_from_markup

        actual = sut.process_markup(mock_link_request_result)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
