import pLinkRequester
import unittest


class MockQueue(object):
    def __init__(self):
        self.data = []

    def put(self, item):
        self.data.append(item)

    def get(self):
        return None


class PLinkRequester_AddWorkTests(unittest.TestCase):
    def test_RaisesTypeErrorIfItemIsNone(self):
        sut = pLinkRequester.PLinkRequester(1, None, None, None)

        self.assertRaises(TypeError, sut.add_work, None)

    def test_AddWorkAddsItemToInputQueue(self):
        dummyQueue = MockQueue()
        dummyItem = "x"
        sut = pLinkRequester.PLinkRequester(1, None, dummyQueue, None)

        sut.add_work(dummyItem)

        self.assertEqual(dummyItem, dummyQueue.data[0])


if __name__ == '__main__':
    unittest.main()
