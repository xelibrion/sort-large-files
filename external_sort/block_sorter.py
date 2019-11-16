from typing import List
import io

from tqdm import tqdm


def _sort_block(block: List[str], block_idx: int, temp_dir: str) -> str:
    block.sort()
    file_name = f'{temp_dir}/_block_{block_idx}.txt'
    with open(file_name, 'w') as block_file:
        block_file.write('\n'.join(block))
    return file_name


class BlockSorter:
    def __init__(self, max_block_size, temp_dir='.tmp'):
        self.max_block_size = max_block_size
        self.temp_dir = temp_dir

    def __call__(self, input_file: io.TextIOWrapper) -> List[str]:
        block = []
        # NOTE: assuming there's enough memory to hold all file paths
        # otherwise can write them into a file one-by-one
        block_files = []
        total_lines = 0

        with tqdm(desc='Sorting blocks') as tq:
            for line in input_file:
                block.append(line.strip('\n'))
                if len(block) == self.max_block_size:
                    block_files.append(_sort_block(block, len(block_files),
                                                   self.temp_dir))
                    tq.update()
                    total_lines += self.max_block_size

                    block = []

            block_files.append(_sort_block(block, len(block_files), self.temp_dir))
            tq.update()

        return block_files, total_lines + len(block)
