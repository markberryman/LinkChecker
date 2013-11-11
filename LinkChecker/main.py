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
import linkRequester
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
link_request_processor = linkRequestProcessor.LinkRequestProcessor(
    url_requester, response_processor)
link_filters = [linkFilter.MailToFilter(), linkFilter.DomainCheckFilter(startLink.url)]
link_transformers = [linkTransform.RelativeLinkTransform(),
                    linkTransform.LowerCaseTransform()]
html_link_parser = htmlLinkParser.HTMLLinkParser()
link_filter_processor = linkFilterProcessor.LinkFilterProcessor(link_filters)
link_transform_processor = linkTransformProcessor.LinkTransformProcessor(
    link_transformers)
links_post_processor = linksPostProcessor.LinksPostProcessor(
    link_filter_processor, link_transform_processor)
link_processor = linkProcessor.LinkProcessor(
    html_link_parser, links_post_processor)
p_link_requester = linkRequester.LinkRequester(
    25, link_request_processor.process_link_request, queue.Queue(), queue.Queue())

checker = linkChecker.LinkChecker(
    link_processor, p_link_requester, depth)

results = checker.check_links(startLink)

checker.print_results(results)

input('Press Enter to exit')
