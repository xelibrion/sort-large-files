import string
import random
import os
from multiprocessing import Pool
from tqdm import tqdm


def _random_string(max_line_length):
    num_chars = random.randint(1, max_line_length)
    chars = random.choices(string.ascii_lowercase, k=num_chars)
    return ''.join(chars)


def _generate_block(input_tuple):
    block_size, max_line_length = input_tuple
    block = [_random_string(max_line_length) for _ in range(block_size)]
    return '\n'.join(block)


def generate(num_lines: int, max_line_length: int, block_size=10000):
    with open('./large_file.txt', 'w') as out_f:
        with Pool(os.cpu_count()) as pool:

            t = tqdm(desc='Generating lines', total=num_lines)

            args = ((block_size, max_line_length) for _ in range(num_lines // block_size))
            for result in pool.imap_unordered(_generate_block, args):
                out_f.write(result)
                out_f.write('\n')

                t.update(block_size)
