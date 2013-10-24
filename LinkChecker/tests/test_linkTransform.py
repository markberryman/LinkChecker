import link
import linkTransform
import unittest


class LinkTransform_TransformTests(unittest.TestCase):
    def test_RaisesTypeErrorIfProcessingContextIsNone(self):
        sut = linkTransform.LinkTransform()

        self.assertRaises(TypeError, sut.transform, None, "some link")

    def test_RaisesTypeErrorIfLinkIsNone(self):
        sut = linkTransform.LinkTransform()

        self.assertRaises(TypeError, sut.transform, "some context", None)


class LowerCaseTransformUnitTests(unittest.TestCase):
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
