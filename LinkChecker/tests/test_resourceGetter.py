import link
import linkRequest
import linkRequestResult
import resourceGetter
import unittest


class MockResponse(object):
    def __init__(self):
        self.status = 200

    def read(self):
        return b"hi"


class MockRequester(object):
    def request_url(self, url):
        return MockResponse()


class ResourceGetter_GetResourceTests(unittest.TestCase):
    def test_RaisesTypeErrorIflinkToProcessIsNone(self):
        sut = resourceGetter.ResourceGetter(None)

        self.assertRaises(TypeError, sut.get_resource, None)

    def test_SetsResponseStatusCodeAndResponseDataForAnchorTag(self):
        mockRequester = MockRequester()
        dummyLinkRequest = linkRequest.LinkRequest("url", True)
        sut = resourceGetter.ResourceGetter(mockRequester)
        expected = linkRequestResult.LinkRequestResult(
            dummyLinkRequest.link_url, 200, "hi")

        actual = sut.get_resource(dummyLinkRequest)

        self.assertEqual(expected.status_code, actual.status_code)
        self.assertEqual(expected.response, actual.response)

    def test_SetsResponseToNoneForLinkRequestNotReadingResponse(self):
        mockRequester = MockRequester()
        dummyLinkRequest = linkRequest.LinkRequest("url", False)
        sut = resourceGetter.ResourceGetter(mockRequester)
        expected = linkRequestResult.LinkRequestResult(None, None, None)

        actual = sut.get_resource(dummyLinkRequest)

        self.assertEqual(expected.response, actual.response)

if __name__ == '__main__':
    unittest.main()
