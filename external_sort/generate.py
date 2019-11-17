import string
import random
import os
from multiprocessing import Pool
from itertools import chain

from tqdm import tqdm


def _random_string(max_line_length):
    num_chars = random.randint(1, max_line_length)
    chars = random.choices(string.ascii_lowercase, k=num_chars)
    return ''.join(chars)


def _generate_block(input_tuple):
    block_size, max_line_length = input_tuple
    block = [_random_string(max_line_length) for _ in range(block_size)]
    return '\n'.join(block), block_size


def generate(num_lines: int, max_line_length: int, block_size=10000):
    with open('./large_file.txt', 'w') as out_f:
        with Pool(os.cpu_count()) as pool:
            with tqdm(desc='Generating lines', total=num_lines) as tq:
                args = ((block_size, max_line_length)
                        for _ in range(num_lines // block_size))
                final = ((num_lines % block_size, max_line_length) for _ in range(1))

                for result, size in pool.imap_unordered(_generate_block,
                                                        chain(args, final)):
                    if size:
                        out_f.write(result)
                        out_f.write('\n')
                        tq.update(size)
