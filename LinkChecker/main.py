import urlRequester
import htmlLinkParser
import httpConnWrapper
import link
import linkChecker
import linkFilter
import linkFilterProcessor
import linkProcessor
import linkRequestProcessor
import linkTransform
import linkTransformProcessor
import pLinkRequester
import responseProcessor
import queue

import urlParseWrapper

startLink = link.Link(
    #"http://www.microsoft.com/en-us/default.aspx")
    #"http://www.markwberryman.com/")
    "http://apigee.com/about/customers/bechtel-improving-workforce-efficiency-and-productivity-through-apis")

depth = 2

print("Starting link checking with \"{}\" and depth {}".format(
    startLink.url, depth))

http_conn_wrapper = httpConnWrapper.HttpConnWrapper()
url_parse_wrapper = urlParseWrapper.UrlParseWrapper()
contRequester = urlRequester.UrlRequester(
    http_conn_wrapper, url_parse_wrapper)
response_processor = responseProcessor.ResponseProcessor()
linkRequestProcessor = linkRequestProcessor.LinkRequestProcessor(
    contRequester, response_processor)
linkFilters = set(
    [linkFilter.MailToFilter(), linkFilter.DomainCheckFilter(startLink.url)])
linkTransformers = [linkTransform.RelativeLinkTransform(),
                    linkTransform.LowerCaseTransform()]
html_link_parser = htmlLinkParser.HTMLLinkParser()
linkFilterProcessor = linkFilterProcessor.LinkFilterProcessor(linkFilters)
linkTransformProcessor = linkTransformProcessor.LinkTransformProcessor(
    linkTransformers)
linkProcessor = linkProcessor.LinkProcessor(
    linkFilterProcessor, linkTransformProcessor, html_link_parser)
pLinkRequester = pLinkRequester.PLinkRequester(
    25, linkRequestProcessor.process_link_request, queue.Queue(), queue.Queue())

checker = linkChecker.LinkChecker(
    linkProcessor, pLinkRequester, depth)

results = checker.check_links(startLink)

checker.print_results(results)

input('Press Enter to exit')
