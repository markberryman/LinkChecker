import urlRequester
import htmlLinkParser
import httpConnWrapper
from link import link
import linkChecker
import linksPostProcessor
import linkProcessor
from linkrequest import linkRequestProcessor
from modifiers import linkFilter
from modifiers import linkFilterProcessor
from modifiers import linkTransform
from modifiers import linkTransformProcessor
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
url_requester = urlRequester.UrlRequester(
    http_conn_wrapper, url_parse_wrapper)
response_processor = responseProcessor.ResponseProcessor()
linkRequestProcessor = linkRequestProcessor.LinkRequestProcessor(
    url_requester, response_processor)
linkFilters = set(
    [linkFilter.MailToFilter(), linkFilter.DomainCheckFilter(startLink.url)])
linkTransformers = [linkTransform.RelativeLinkTransform(),
                    linkTransform.LowerCaseTransform()]
html_link_parser = htmlLinkParser.HTMLLinkParser()
linkFilterProcessor = linkFilterProcessor.LinkFilterProcessor(linkFilters)
linkTransformProcessor = linkTransformProcessor.LinkTransformProcessor(
    linkTransformers)
links_post_processor = linksPostProcessor.LinksPostProcessor(
    linkFilterProcessor, linkTransformProcessor)
linkProcessor = linkProcessor.LinkProcessor(
    html_link_parser, links_post_processor)
pLinkRequester = pLinkRequester.PLinkRequester(
    25, linkRequestProcessor.process_link_request, queue.Queue(), queue.Queue())

checker = linkChecker.LinkChecker(
    linkProcessor, pLinkRequester, depth)

results = checker.check_links(startLink)

checker.print_results(results)

input('Press Enter to exit')
