import linksPostProcessor
import unittest
from unittest.mock import MagicMock


class LinksPostProcessor_ApplyTransformsAndFiltersTests(unittest.TestCase):
    def test_TransformsApplied(self):
        dummy_links = "links"
        dummy_processing_context = "context"
        mock_link_transform_processor = MagicMock()
        sut = linksPostProcessor.LinksPostProcessor(
            None, mock_link_transform_processor)

        sut.apply_transforms_and_filters(
            dummy_links, dummy_processing_context)

        mock_link_transform_processor.apply_transformers.assert_called_with(
            dummy_processing_context, dummy_links)

    def test_FiltersApplied(self):
        dummy_links = "links"
        mock_link_filter_processor = MagicMock()
        sut = linksPostProcessor.LinksPostProcessor(
            mock_link_filter_processor, None)

        sut.apply_transforms_and_filters(
            dummy_links, None)

        mock_link_filter_processor.apply_filters.assert_called_with(
            dummy_links)

    # todo - figure out the best way to verify ordered calls
    # maybe use side-effects?
    #def test_TransformsAppliedBeforeFilters(self):
    #    self.fail("Not implemented")

    def test_ReturnsLinksReturnedByLinkFilterProcessor(self):
        dummy_links = "links"
        mock_link_filter_processor = MagicMock()
        mock_link_filter_processor.apply_filters = MagicMock(return_value=dummy_links)
        sut = linksPostProcessor.LinksPostProcessor(
            mock_link_filter_processor, None)
        expected = dummy_links

        actual = sut.apply_transforms_and_filters(
            dummy_links, None)

        self.assertEqual(expected, actual)
    

if __name__ == '__main__':
    unittest.main()
