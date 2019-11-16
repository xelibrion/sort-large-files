from typing import List
from heapq import heapify, heappushpop, heappop
import shutil
import io

from tqdm import tqdm


class FileMerger:
    def __init__(self,
                 output_file: str,
                 max_files: int,
                 buffer_size: int,
                 temp_dir='.tmp'):
        self.output_file = output_file
        self.max_files = max_files
        self.buffer_size = buffer_size
        self.temp_dir = '.tmp'

    def __call__(self, block_files: List[str], total_lines: int):
        num_iter = 0
        while len(block_files) > 1:
            merge_block = block_files[:self.max_files]
            block_files = block_files[self.max_files:]

            result_file = self._do_merge(
                merge_block,
                num_iter,
                total_lines,
            )
            num_iter += 1
            block_files.append(result_file)

        shutil.move(block_files[0], self.output_file)
        print(f"Sorted output is now stored in '{self.output_file}'")

    def _merge_to_buffer(
            self,
            handles: List[io.TextIOWrapper],
            file_block_idx: int,
            total_lines: int,
    ):
        # NOTE: the progress indicator will only go to a 100%
        # for the final merge, intermediate ones will be abandoned halfway through
        with tqdm(
                desc=f'Merging file block #{file_block_idx}, lines',
                total=total_lines,
        ) as tq:
            heap = [(h.readline().strip('\n'), idx) for idx, h in enumerate(handles)]
            heapify(heap)

            buffer = []

            while heap:
                line, handle_idx = heap[0]
                buffer.append(line)

                if len(buffer) == self.buffer_size:
                    yield buffer
                    buffer = []

                new_line = handles[handle_idx].readline().strip('\n')
                if new_line:
                    heappushpop(heap, (new_line, handle_idx))
                else:
                    heappop(heap)
                tq.update()

            yield buffer

    def _do_merge(
            self,
            files: List[str],
            file_block_idx: int,
            total_lines: int,
    ):
        out_filename = f'{self.temp_dir}/_merge_{file_block_idx}.txt'

        handles = [open(x) for x in files]
        with open(out_filename, 'w') as out_f:
            for buffer in self._merge_to_buffer(handles, file_block_idx, total_lines):
                out_f.write('\n'.join(buffer))
                out_f.write('\n')

        for h in handles:
            h.close()

        return out_filename
