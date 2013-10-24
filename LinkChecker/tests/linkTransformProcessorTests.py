import link
import linkTransformProcessor
import unittest


class MockTransform(object):
    def __init__(self):
        self.transformFnCalled = False

    def transform(self, currentLink, link):
        self.transformFnCalled = True


class LinkTransformProcessor_ApplyTransformersTests(unittest.TestCase):
    def test_RaisesTypeErrorIfContextIsNone(self):
        sut = linkTransformProcessor.LinkTransformProcessor(None)

        self.assertRaises(TypeError, sut.apply_transformers, None, "some link")

    def test_RaisesTypeErrorIfNewLinksIsNone(self):
        sut = linkTransformProcessor.LinkTransformProcessor(None)

        self.assertRaises(TypeError, sut.apply_transformers, "some context", None)

    def test_AppliesAllTransforms(self):
        dummyTransformA = MockTransform()
        dummyTransformB = MockTransform()
        dummyTransformers = [dummyTransformA, dummyTransformB]
        dummyLinks = [link.Link("a link")]
        sut = linkTransformProcessor.LinkTransformProcessor(dummyTransformers)

        sut.apply_transformers("current link", dummyLinks)

        self.assertTrue(dummyTransformA.transformFnCalled)
        self.assertTrue(dummyTransformB.transformFnCalled)


if __name__ == '__main__':
    unittest.main()
