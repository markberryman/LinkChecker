from unittest.mock import call
from link import link
from modifiers import linkFilter
from modifiers import linkFilterProcessor
from unittest.mock import MagicMock
import unittest


class LinkFilterProcessor_ApplyFiltersTests(unittest.TestCase):
    def test_RaisesTypeErrorIfLinksIsNone(self):
        sut = linkFilterProcessor.LinkFilterProcessor(None)

        self.assertRaises(TypeError, sut.apply_filters, None)

    def test_AppliesFiltersToEveryLinkIfNotFiltered(self):
        mockFilter1 = linkFilter.LinkFilter()
        mockFilter2 = linkFilter.LinkFilter()
        mockFilter1.should_filter = MagicMock(return_value=False)
        mockFilter2.should_filter = MagicMock(return_value=False)
        link1 = link.Link("link1")
        link2 = link.Link("link2")
        dummyLinks = set([link1, link2])
        sut = linkFilterProcessor.LinkFilterProcessor(
            [mockFilter1, mockFilter2])

        sut.apply_filters(dummyLinks)

        mockFilter1.should_filter.assert_has_calls(
            [call("link1"), call("link2")], any_order=True)
        mockFilter2.should_filter.assert_has_calls(
            [call("link1"), call("link2")], any_order=True)
    
    def test_FiltersLinks(self):
        mockFilter1 = linkFilter.LinkFilter()
        mockFilter1.should_filter = MagicMock(return_value=True)
        link1 = link.Link("link1")
        dummyLinks = set([link1])
        expected = 0
        sut = linkFilterProcessor.LinkFilterProcessor([mockFilter1])

        actual = sut.apply_filters(dummyLinks)

        self.assertEqual(expected, len(actual))
            
    def test_ReturnsUnfilteredLinks(self):
        mockFilter1 = linkFilter.LinkFilter()
        mockFilter1.should_filter = MagicMock(return_value=False)
        link1 = link.Link("link1")
        link2 = link.Link("link2")
        dummyLinks = set([link1, link2])
        expected = dummyLinks
        sut = linkFilterProcessor.LinkFilterProcessor([mockFilter1])

        actual = sut.apply_filters(dummyLinks)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
