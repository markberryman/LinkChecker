import urlRequester
import htmlLinkParser
import link
import linkChecker
import linkFilter
import linkFilterProcessor
import linkTransform
import linkTransformProcessor
import linkProcessor
import pLinkRequester
import queue
import resourceGetter
import unittest


# these are more functional tests rather than unit tests
class LinkChecker_CheckLinksTests(unittest.TestCase):
    def test_FunctionalE2ETest(self):
        baseStartUrl = "http://localhost:35944"
        startLink = link.Link(baseStartUrl + "/index.html")
        depth = 3
        contRequester = urlRequester.UrlRequester()
        resGetter = resourceGetter.ResourceGetter(contRequester)
        linkFilters = set(
            [linkFilter.MailToFilter(),
                linkFilter.DomainCheckFilter(startLink.url)])
        linkTransformers = [linkTransform.RelativeLinkTransform(),
                            linkTransform.LowerCaseTransform()]
        html_link_parser = htmlLinkParser.HTMLLinkParser()
        lfp = linkFilterProcessor.LinkFilterProcessor(linkFilters)
        lt = linkTransformProcessor.LinkTransformProcessor(linkTransformers)
        lp = linkProcessor.LinkProcessor(lfp, lt, html_link_parser)
        plr = pLinkRequester.PLinkRequester(
            3, resGetter.get_resource, queue.Queue(), queue.Queue())
        sut = linkChecker.LinkChecker(resGetter, lp, plr, depth)

        results = sut.check_links(startLink)

        linksRequested = results["linksRequested"]
        self.assertEqual(11, len(linksRequested))
        self.assertEqual(3, len(results["brokenLinks"]))
        self.assertEqual(1, len(results["invalidMarkupLinks"]))
        self.assertTrue(
            baseStartUrl + "/arelativelink.html" in linksRequested)
        self.assertTrue(
            baseStartUrl + "/subdir/arelativelinkinasubdir.html"
            in linksRequested)

    def test_SimpleDepthProcessingTest(self):
        baseStartUrl = "http://localhost:35944/SimpleDepthProcessingTest"
        startLink = link.Link(baseStartUrl + "/depth1.html")
        depth = 3
        contRequester = urlRequester.UrlRequester()
        resGetter = resourceGetter.ResourceGetter(contRequester)
        html_link_parser = htmlLinkParser.HTMLLinkParser()
        lp = linkProcessor.LinkProcessor(None, None, html_link_parser)
        plr = pLinkRequester.PLinkRequester(
            3, resGetter.get_resource, queue.Queue(), queue.Queue())
        sut = linkChecker.LinkChecker(resGetter, lp, plr, depth)

        results = sut.check_links(startLink)

        linksRequested = results["linksRequested"]
        self.assertEqual(3, len(linksRequested))


if __name__ == '__main__':
    unittest.main()
