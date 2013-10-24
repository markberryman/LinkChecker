import linkProcessor
import unittest


class LinkProcessor_ProcessLinkTests(unittest.TestCase):
    def test_RaisesTypeErrorIfLinkToProcessIsNone(self):
        sut = linkProcessor.LinkProcessor(None, None, None)

        self.assertRaises(TypeError, sut.process_link, None)


if __name__ == '__main__':
    unittest.main()
