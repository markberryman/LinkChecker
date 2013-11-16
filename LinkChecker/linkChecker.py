from link import linkType
from linkrequest import linkRequest


class LinkChecker:
    def __init__(
            self, link_requester, 
            link_request_result_processor, max_depth):
        self._links_requested = set()
        self._broken_links = set()
        self._invalid_markup_links = set()
        self._link_requester = link_requester
        self._link_request_result_processor = link_request_result_processor
        self._max_depth = max_depth

    def print_results(self, results):
        print("")
        print("Results:")
        print("Number of links checked = {}".
              format(len(results["linksRequested"])))

        self._print_links(results["linksRequested"])

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
            self._print_links(results["invalidMarkupLinks"])

    def _print_links(self, links):
        links = sorted(links)

        for l in links:
            print("* {}".format(l))

    def _create_requests(self, links_to_process, is_leaf_request):
        for link in links_to_process:
            # don't need to read response for last link depth (aka leaf requests)
            shouldReadResponse = (
                (link.type == linkType.LinkType.ANCHOR) and
                (is_leaf_request is False)
                )
            linkRequestWorkItem = linkRequest.LinkRequest(link.url, shouldReadResponse)
            self._link_requester.add_work(linkRequestWorkItem)
            self._links_requested.add(link.url)

        links_to_process.clear()

    def _check_links_helper(self, links_to_process):
        # breadth-first search of links
        for depth in range(1, self._max_depth + 1):
            if (len(links_to_process) == 0):
                break

            print("\nProcessing {} link(s) at depth {}."
                  .format(len(links_to_process), depth))

            self._create_requests(links_to_process, depth == self._max_depth)

            # get results; blocking until all link processing completed
            print("\nAwaiting results...\n")
            linkRequestResults = self._link_requester.get_results()

            good_links, invalid_markup_links, broken_links = self._link_request_result_processor.process_link_request_result(
                linkRequestResults)

            # filter out links previously requested
            links_to_process.extend(
                good_links.difference(self._links_requested))

            self._invalid_markup_links = self._invalid_markup_links.union(invalid_markup_links)

            self._broken_links = self._broken_links.union(broken_links)

    def check_links(self, start_link):
        self._link_requester.start()
        self._check_links_helper([start_link])

        return {
            "linksRequested": self._links_requested,
            "brokenLinks": self._broken_links,
            "invalidMarkupLinks": self._invalid_markup_links
            }
