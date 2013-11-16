import linkRequester
import unittest
from unittest.mock import MagicMock


class LinkRequester_WorkerTests(unittest.TestCase):
    # not defining unit tests for this method b/c of the
    # while True loop; how to break out of this from
    # within a test?
    pass


class LinkRequester_AddWorkTests(unittest.TestCase):
    def test_RaisesTypeErrorIfItemIsNone(self):
        sut = linkRequester.LinkRequester(1, None, None, None)

        self.assertRaises(TypeError, sut.add_work, None)

    def test_AddWorkAddsItemToInputQueue(self):
        dummy_link_request = "dlr"
        mock_queue = MagicMock()
        sut = linkRequester.LinkRequester(
            None, None, mock_queue, None)

        sut.add_work(dummy_link_request)

        mock_queue.put.assert_called_with(dummy_link_request)


class LinkRequester_GetResultsTests(unittest.TestCase):
    def test_CallsJoinOnInputQueue(self):
        mock_input_queue = MagicMock()
        mock_output_queue = MagicMock()
        sut = linkRequester.LinkRequester(
            None, None, mock_input_queue, mock_output_queue)

        sut.get_results()

        mock_input_queue.join.assert_called_with()

    def test_ReturnsResultsInOutputQueue(self):
        mock_input_queue = MagicMock()
        mock_output_queue = MagicMock()
        mock_output_queue.empty = MagicMock(side_effect=[False, False, True])
        mock_output_queue.get = MagicMock(side_effect=["a", "b"])
        sut = linkRequester.LinkRequester(
            None, None, mock_input_queue, mock_output_queue)
        expected = ["a", "b"]

        actual = sut.get_results()

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
