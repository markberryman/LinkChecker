import urlRequester
import htmlLinkParser
import httpConnWrapper
import link
import linkChecker
from modifiers import linkFilter
from modifiers import linkFilterProcessor
import linksPostProcessor
import linkRequestProcessor
from modifiers import linkTransform
from modifiers import linkTransformProcessor
import linkProcessor
import pLinkRequester
import responseProcessor
import queue
import unittest
import urlParseWrapper


# these are more functional tests rather than unit tests
class LinkChecker_CheckLinksTests(unittest.TestCase):
    def test_FunctionalE2ETest(self):
        base_start_url = "http://localhost:35944"
        start_link = link.Link(base_start_url + "/index.html")
        depth = 3
        http_conn_wrapper = httpConnWrapper.HttpConnWrapper()
        url_parse_wrapper = urlParseWrapper.UrlParseWrapper()
        url_requester = urlRequester.UrlRequester(
            http_conn_wrapper, url_parse_wrapper)
        response_processor = responseProcessor.ResponseProcessor()
        link_request_processor = linkRequestProcessor.LinkRequestProcessor(
            url_requester, response_processor)
        link_filters = set(
            [linkFilter.MailToFilter(),
                linkFilter.DomainCheckFilter(start_link.url)])
        link_transformers = [linkTransform.RelativeLinkTransform(),
                            linkTransform.LowerCaseTransform()]
        html_link_parser = htmlLinkParser.HTMLLinkParser()
        link_filter_processor = linkFilterProcessor.LinkFilterProcessor(link_filters)
        link_transform_processor = linkTransformProcessor.LinkTransformProcessor(link_transformers)
        links_post_processor = linksPostProcessor.LinksPostProcessor(
            link_filter_processor, link_transform_processor)
        link_processor = linkProcessor.LinkProcessor(
            html_link_parser, links_post_processor)
        parallel_link_requester = pLinkRequester.PLinkRequester(
            3, link_request_processor.process_link_request, queue.Queue(), queue.Queue())
        sut = linkChecker.LinkChecker(link_processor, parallel_link_requester, depth)

        results = sut.check_links(start_link)

        links_requested = results["linksRequested"]
        self.assertEqual(11, len(links_requested))
        self.assertEqual(3, len(results["brokenLinks"]))
        self.assertEqual(1, len(results["invalidMarkupLinks"]))
        self.assertTrue(
            base_start_url + "/arelativelink.html" in links_requested)
        self.assertTrue(
            base_start_url + "/subdir/arelativelinkinasubdir.html"
            in links_requested)

    def test_SimpleDepthProcessingTest(self):
        base_start_url = "http://localhost:35944/SimpleDepthProcessingTest"
        start_link = link.Link(base_start_url + "/depth1.html")
        depth = 3
        http_conn_wrapper = httpConnWrapper.HttpConnWrapper()
        url_parse_wrapper = urlParseWrapper.UrlParseWrapper()
        url_requester = urlRequester.UrlRequester(
            http_conn_wrapper, url_parse_wrapper)
        response_processor = responseProcessor.ResponseProcessor()
        link_request_processor = linkRequestProcessor.LinkRequestProcessor(
            url_requester, response_processor)
        html_link_parser = htmlLinkParser.HTMLLinkParser()
        link_processor = linkProcessor.LinkProcessor(
            html_link_parser, None)
        parallel_link_requester = pLinkRequester.PLinkRequester(
            3, link_request_processor.process_link_request, queue.Queue(), queue.Queue())
        sut = linkChecker.LinkChecker(link_processor, parallel_link_requester, depth)

        results = sut.check_links(start_link)

        links_requested = results["linksRequested"]
        self.assertEqual(3, len(links_requested))


if __name__ == '__main__':
    unittest.main()
