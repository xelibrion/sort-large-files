import unittest
from unittest.mock import patch, mock_open, MagicMock

from external_sort.file_merger import FileMerger


class StubHandle:
    def __init__(self, data):
        self.data = data
        self.position = 0

    def readline(self):
        if self.position >= len(self.data):
            return ''

        line = self.data[self.position]
        self.position += 1
        return line


handles = [
    StubHandle(data=['1\n', '2\n', '3\n', '4\n', '5']),
    StubHandle(data=['a\n', 'b\n', 'c\n', 'd\n', 'e\n', 'f\n', 'h']),
]


class FileMergerTests(unittest.TestCase):
    def test_should_publish_incomplete_buffers(self):
        m = FileMerger(None, max_files=2, buffer_size=3)

        handles = [
            StubHandle(data=['1\n', '2\n']),
            StubHandle(data=['a\n', 'b\n']),
        ]
        buffers = list(m._merge_to_buffer(handles, 0, 0))
        self.assertEqual(2, len(buffers))
        self.assertEqual(3, len(buffers[0]))
        self.assertEqual(1, len(buffers[1]))

    def test_should_strip_new_line_separators(self):
        m = FileMerger(None, max_files=2, buffer_size=3)

        handles = [
            StubHandle(data=['1\n', '2\n']),
            StubHandle(data=['a\n', 'b\n']),
        ]
        buffers = list(m._merge_to_buffer(handles, 0, 0))
        self.assertEqual(['1', '2', 'a'], buffers[0])

    def test_should_output_lines_in_correct_order(self):
        m = FileMerger(None, max_files=2, buffer_size=5)

        handles = [
            StubHandle(data=['a\n', 'b\n', 'c']),
            StubHandle(data=['a\n', 'b\n']),
        ]
        buffers = list(m._merge_to_buffer(handles, 0, 0))
        self.assertEqual(['a', 'a', 'b', 'b', 'c'], buffers[0])
