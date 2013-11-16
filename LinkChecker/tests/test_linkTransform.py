from link import link
from modifiers import linkTransform
import unittest


class LinkTransform_EmptyPathTransformTests(unittest.TestCase):
    def test_TrimsTrailingSlashForEmptyPath(self):
        dummy_link = link.Link("http://foo.com/")
        expected = "http://foo.com"
        sut = linkTransform.EmptyPathTransform()

        sut.transform(None, dummy_link)

        self.assertEqual(expected, dummy_link.url)


class LinkTransform_LowerCaseTransformUnitTests(unittest.TestCase):
    def test_OnlyLowerCasesUrlSchemeAndNetloc(self):
        dummyLink = link.Link("HTTP://WWW.FOO.COM/SOMEPATH/INDEX.HTML?A=FOO")
        expected = "http://www.foo.com/SOMEPATH/INDEX.HTML?A=FOO"
        sut = linkTransform.LowerCaseTransform()

        sut.transform(None, dummyLink)

        self.assertEqual(expected, dummyLink.url)


class LinkTransform_RelativeLinkTransformTests(unittest.TestCase):           
    # only need a single sanity unit test here since the transform
    # is pretty much just running urljoin
    def test_TransformsLinkWithNetlocAndOnlySlashForPath(self):
        dummyContext = {
            "current_link_url": "http://www.foo.com/"
            }
        dummyNewLink = link.Link("relativelink.html")
        sut = linkTransform.RelativeLinkTransform()

        sut.transform(dummyContext, dummyNewLink)

        self.assertEqual(
            dummyNewLink.url, "http://www.foo.com/relativelink.html")



if __name__ == '__main__':
    unittest.main()
