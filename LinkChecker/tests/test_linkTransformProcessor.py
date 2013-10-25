import link
import linkTransform
import linkTransformProcessor
import unittest
from unittest.mock import call
from unittest.mock import MagicMock


class LinkTransformProcessor_ApplyTransformersTests(unittest.TestCase):
    def test_RaisesTypeErrorIfProcessingContextIsNone(self):
        sut = linkTransformProcessor.LinkTransformProcessor(None)

        self.assertRaises(TypeError, sut.apply_transformers, None, "some link")

    def test_RaisesTypeErrorIfLinksIsNone(self):
        sut = linkTransformProcessor.LinkTransformProcessor(None)

        self.assertRaises(TypeError, sut.apply_transformers, "some context", None)

    def test_AppliesAllTransformsToAllLinks(self):
        mock_transform_1 = linkTransform.LinkTransform()
        mock_transform_2 = linkTransform.LinkTransform()
        mock_transform_1.transform = MagicMock()
        mock_transform_2.transform = MagicMock()
        dummy_processing_context = dict()
        link1 = link.Link("link1")
        link2 = link.Link("link2")
        dummy_links = set([link1, link2])
        sut = linkTransformProcessor.LinkTransformProcessor(
            [mock_transform_1, mock_transform_2])

        sut.apply_transformers(dummy_processing_context, dummy_links)

        mock_transform_1.transform.assert_has_calls(
            [call(dummy_processing_context, link1), 
             call(dummy_processing_context, link2)], 
             any_order=True)
        mock_transform_2.transform.assert_has_calls(
            [call(dummy_processing_context, link1), 
             call(dummy_processing_context, link2)], 
             any_order=True)


if __name__ == '__main__':
    unittest.main()
