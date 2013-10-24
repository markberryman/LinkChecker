import http.client
import html.parser
import link
import linkRequest
import linkType


class LinkChecker:
    def __init__(
            self, resourceGetter, linkProcessor, pLinkRequester, maxDepth):
        self.resourceGetter = resourceGetter
        self.linkProcessor = linkProcessor
        self.linksRequested = set()
        # tuples of link url and status code
        self.brokenLinks = set()
        self.invalidMarkupLinks = set()
        self.pLinkRequester = pLinkRequester
        self.maxDepth = maxDepth

    def print_results(self, results):
        print("")
        print("Results:")
        print("Number of links checked = {}".
              format(len(results["linksRequested"])))

        self.__print_links(results["linksRequested"])

        print("")
        print("Number of broken links = {}".
              format(len(results["brokenLinks"])))

        if (len(results["brokenLinks"]) > 0):
            print("Broken links:")
            for link in results["brokenLinks"]:
                # broken link info comes in a tuple that includes
                # the status code
                print("* {} - {}".format(link[1], link[0]))

        print("")
        print("Number of links with invalid markup = {}".
              format(len(results["invalidMarkupLinks"])))

        if (len(results["invalidMarkupLinks"]) > 0):
            print("Invalid markup links:")
            self.__print_links(results["invalidMarkupLinks"])

    def __print_links(self, links):
        links = sorted(links)

        for l in links:
            print("* {}".format(l))

    @staticmethod
    def _is_link_broken(status_code):
        return ((status_code < http.client.OK) or
                (status_code >= http.client.BAD_REQUEST))

    def _process_link_request_result(self, link_request_result):
        """Determine the new links to request from a link request result."""
        new_links = self.linkProcessor.process_link(link_request_result)
        links_to_process = new_links.difference(self.linksRequested)

        return links_to_process

    def _create_requests(self, links_to_process, is_leaf_request):
        for link in links_to_process:
            # don't need to read response for last link depth (aka leaf requests)
            shouldReadResponse = ((link.type == linkType.LinkType.ANCHOR) and
                                    (is_leaf_request is False))
            linkRequestWorkItem = linkRequest.LinkRequest(link.url, shouldReadResponse)
            self.pLinkRequester.add_work(linkRequestWorkItem)
            self.linksRequested.add(link.url)

        links_to_process.clear()

    def __check_links_helper(self, linksToProcess):
        # breadth-first search of links
        for depth in range(1, self.maxDepth + 1):
            print("\nProcessing {} link(s) at depth {}."
                  .format(len(linksToProcess), depth))

            self._create_requests(linksToProcess, depth == self.maxDepth)

            # get results; blocking until all link processing completed
            print("\nAwaiting results...\n")
            linkRequestResults = self.pLinkRequester.get_results()

            for linkRequestResult in linkRequestResults:
                result_status_code = linkRequestResult.status_code
                print("[{}] {}\n  --> {}".format(result_status_code,
                                          http.client.responses[result_status_code].upper(),
                                          linkRequestResult.link_url))                

                if (LinkChecker._is_link_broken(result_status_code) is False):
                    if (linkRequestResult.response is not None):
                        try:
                            new_links = self._process_link_request_result(linkRequestResult)
                            linksToProcess.extend(list(new_links))
                        except html.parser.HTMLParseError:
                            self.invalidMarkupLinks.add(linkRequestResult.link_url)
                else:
                    self.brokenLinks.add((
                        linkRequestResult.link_url, linkRequestResult.status_code))

    def check_links(self, startLink):
        self.pLinkRequester.start()
        self.__check_links_helper([startLink])

        return {
            "linksRequested": self.linksRequested,
            "brokenLinks": self.brokenLinks,
            "invalidMarkupLinks": self.invalidMarkupLinks
            }
