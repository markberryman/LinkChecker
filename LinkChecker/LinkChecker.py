from link import linkType
from linkrequest import linkRequest


class LinkChecker:
    def __init__(
            self, linkProcessor, link_requester, 
            link_request_result_processor, maxDepth):
        self.linkProcessor = linkProcessor
        self.linksRequested = set()
        # tuples of link url and status code
        self.brokenLinks = set()
        self.invalidMarkupLinks = set()
        self._link_requester = link_requester
        self._link_request_result_processor = link_request_result_processor
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

    def _create_requests(self, links_to_process, is_leaf_request):
        for link in links_to_process:
            # don't need to read response for last link depth (aka leaf requests)
            shouldReadResponse = ((link.type == linkType.LinkType.ANCHOR) and
                                    (is_leaf_request is False))
            linkRequestWorkItem = linkRequest.LinkRequest(link.url, shouldReadResponse)
            self._link_requester.add_work(linkRequestWorkItem)
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
            linkRequestResults = self._link_requester.get_results()

            good_links, invalid_markup_links, broken_links = self._link_request_result_processor.process_link_request_result(
                linkRequestResults)

            # filter out links previously requested
            linksToProcess.extend(
                good_links.difference(self.linksRequested))

            self.invalidMarkupLinks = self.invalidMarkupLinks.union(invalid_markup_links)

            self.brokenLinks = self.brokenLinks.union(broken_links)

    def check_links(self, startLink):
        self._link_requester.start()
        self.__check_links_helper([startLink])

        return {
            "linksRequested": self.linksRequested,
            "brokenLinks": self.brokenLinks,
            "invalidMarkupLinks": self.invalidMarkupLinks
            }
