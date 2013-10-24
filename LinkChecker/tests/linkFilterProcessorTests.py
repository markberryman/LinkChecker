import link
import linkFilterProcessor
import unittest


class MockFilter(object):
    def __init__(self, filterFn):
        self.filterFn = filterFn

    def should_filter(self, link):
        return self.filterFn(link)


class LinkFilterProcessor_ApplyFiltersTests(unittest.TestCase):
    def test_RaisesTypeErrorIfLinksIsNone(self):
        sut = linkFilterProcessor.LinkFilterProcessor(None)

        self.assertRaises(TypeError, sut.apply_filters, None)

    def test_ReturnsLinksWhenNoFiltersLeftToApply(self):
        dummyFilters = []
        dummyLinks = set([link.Link("a link")])
        sut = linkFilterProcessor.LinkFilterProcessor(dummyFilters)

        result = sut.apply_filters(dummyLinks)

        self.assertEqual(1, len(result))

    def test_AppliesAllFilters(self):
        dummyFilterIsLowerCase = MockFilter(lambda x: x.islower())
        dummyFilterIsUpperCase = MockFilter(lambda x: x.isupper())
        dummyFilters = [dummyFilterIsLowerCase, dummyFilterIsUpperCase]
        dummyLinks = set([
                         link.Link("lowercase"),
                         link.Link("uppercase"),
                         link.Link("MIXEDcase")
                         ])
        sut = linkFilterProcessor.LinkFilterProcessor(dummyFilters)

        result = sut.apply_filters(dummyLinks)

        self.assertEqual(1, len(result))


if __name__ == '__main__':
    unittest.main()
