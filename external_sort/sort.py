import io
import sys
import shutil
import os

from external_sort.block_sorter import BlockSorter
from external_sort.file_merger import FileMerger


def _estimate_line_size_bytes(in_f: io.TextIOWrapper, estimation_block_size=10000) -> int:
    max_byte_size = 0
    for _ in range(estimation_block_size):
        line = in_f.readline()
        max_byte_size = max(max_byte_size, sys.getsizeof(line))

    return max_byte_size


def _get_num_lines_in_block(max_line_size_bytes: int, max_block_size_mb) -> int:
    return max_block_size_mb * 2**20 // max_line_size_bytes


def sort(input_file: str,
         output_file: str,
         sort_max_memory_mb: int = 10,
         merge_max_files: int = 100,
         temp_dir='.tmp'):

    shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir)

    with open(input_file) as in_f:
        line_size_bytes = _estimate_line_size_bytes(in_f)
        in_f.seek(0)

        max_block_length = _get_num_lines_in_block(line_size_bytes, sort_max_memory_mb)
        print(
            f"Max line size (bytes): {line_size_bytes}, allowed block length: {max_block_length}"
        )
        block_files, total_lines = BlockSorter(max_block_length)(in_f)
        merger = FileMerger(output_file, merge_max_files, max_block_length)
        merger(block_files, total_lines)
