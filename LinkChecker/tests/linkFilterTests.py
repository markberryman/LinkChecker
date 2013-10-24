import linkFilter
import unittest


class MailToFilterTests(unittest.TestCase):
    def test_FiltersMailToLinks(self):
        sut = linkFilter.MailToFilter()

        filterResult = sut.should_filter("mailto:foo")

        self.assertTrue(filterResult)


class DomainCheckFilter_ShouldFilterTests(unittest.TestCase):
    def test_ReturnsTrueWhenDomainsDoNotMatch(self):
        sut = linkFilter.DomainCheckFilter("http://www.markwberryman.com")

        filterResult = sut.should_filter("http://www.foo.com")

        self.assertTrue(filterResult)

    def test_ReturnsFalseWhenDomainsMatch(self):
        sut = linkFilter.DomainCheckFilter("http://www.markwberryman.com")

        filterResult = sut.should_filter(
            "http://www.markwberryman.com/index.html")

        self.assertFalse(filterResult)

    def test_ReturnsFalseWhenLinkIsSubDomain(self):
        sut = linkFilter.DomainCheckFilter("http://www.markwberryman.com")

        filterResult = sut.should_filter("http://subdomain.markwberryman.com")

        self.assertFalse(filterResult)

    def test_ReturnsFalseWhenLinkIsNestedSubDomain(self):
        sut = linkFilter.DomainCheckFilter("http://www.markwberryman.com")

        filterResult = sut.should_filter(
            "http://subsubdomain.subdomain.markwberryman.com")

        self.assertFalse(filterResult)

    def test_ReturnsFalseWhenLinkIsSubDomainAndBaseLinkHasTwoSegemnts(self):
        sut = linkFilter.DomainCheckFilter("http://markwberryman.com")

        filterResult = sut.should_filter("http://subdomain.markwberryman.com")

        self.assertFalse(filterResult)

    def test_ReturnsFalseWhenLinkIsHasTwoSegmentsThatMatchDomain(self):
        sut = linkFilter.DomainCheckFilter(
            "http://subdomain.markwberryman.com")

        filterResult = sut.should_filter("http://markwberryman.com")

        self.assertFalse(filterResult)

if __name__ == '__main__':
    unittest.main()
