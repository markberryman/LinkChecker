import urlRequester
import unittest


class UrlRequester_RequestUrlTests(unittest.TestCase):
    def test_RaisesTypeErrorIfUrlIsNone(self):
        sut = urlRequester.UrlRequester()

        self.assertRaises(TypeError, sut.request_url, None)


if __name__ == '__main__':
    unittest.main()
