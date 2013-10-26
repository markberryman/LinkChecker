import pLinkRequester
import unittest
import queue
from unittest.mock import MagicMock


class PLinkRequester_AddWorkTests(unittest.TestCase):
    def test_RaisesTypeErrorIfItemIsNone(self):
        sut = pLinkRequester.PLinkRequester(1, None, None, None)

        self.assertRaises(TypeError, sut.add_work, None)

    def test_AddWorkAddsItemToInputQueue(self):
        mock_queue = queue.Queue()
        mock_queue.put = MagicMock()
        dummy_link_request = MagicMock()
        sut = pLinkRequester.PLinkRequester(
            1, None, mock_queue, None)

        sut.add_work(dummy_link_request)

        mock_queue.put.assert_called_with(dummy_link_request)


if __name__ == '__main__':
    unittest.main()
