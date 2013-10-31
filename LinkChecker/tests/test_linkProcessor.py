import linkProcessor
import unittest
from unittest.mock import MagicMock


class LinkProcessor_ProcessLinkTests(unittest.TestCase):
    def test_RaisesTypeErrorIfLinkRequestResultIsNone(self):
        sut = linkProcessor.LinkProcessor(
            None, None, None, None)

        self.assertRaises(TypeError, sut.process_link, None)

    def test_InvokesLinksPostProcessor(self):
        dummy_link_url = "url"
        mock_link_request_result = MagicMock()
        mock_link_request_result.link_url = dummy_link_url
        mock_html_link_parser = MagicMock()
        dummy_links_from_markup = "links"
        mock_html_link_parser.parse_markup = MagicMock(return_value=dummy_links_from_markup)
        mock_link_transform_processor = MagicMock()
        dummy_processing_context = {
            "current_link_url": dummy_link_url
        }
        mock_links_post_processor = MagicMock()
        sut = linkProcessor.LinkProcessor(
            None, mock_link_transform_processor, mock_html_link_parser, mock_links_post_processor)

        sut.process_link(mock_link_request_result)

        mock_links_post_processor.apply_transforms_and_filters.assert_called_with(
            dummy_links_from_markup, dummy_processing_context)
    
    # test link filter applied
    # test transforms applied before filters
    # test data returned

if __name__ == '__main__':
    unittest.main()
