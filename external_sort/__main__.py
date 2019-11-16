import argparse
from pathlib import Path

from external_sort.generate import generate
from external_sort.sort import sort


def generate_parser(subparsers):
    parser = subparsers.add_parser(
        'generate',
        help="Generate a large file of random strings",
    )
    parser.add_argument(
        'num_lines',
        type=int,
        help="Number of lines in generated file",
    )
    parser.add_argument(
        'max_line_length',
        type=int,
        help="Maximum length of a string in the file",
    )


def sort_parser(subparsers):
    parser = subparsers.add_parser('sort', help='Sort a file')
    parser.add_argument(
        '--input-file',
        type=Path,
        default=Path('./large_file.txt'),
        help="Path to input file",
    )
    parser.add_argument(
        '--output-file',
        type=Path,
        default=Path('./sorted.txt'),
        help="Path to output file",
    )
    parser.add_argument(
        '--sort-max-memory-mb',
        type=int,
        default=10,
        help="Amount of memory allowed for sorting",
    )
    parser.add_argument(
        '--merge-max-files',
        type=int,
        default=100,
        help="Number of files to be merged at once during merge stage",
    )


def main():
    parser = argparse.ArgumentParser(description="Sort large files")
    subparsers = parser.add_subparsers(
        title='commands',
        help='Command to run',
        dest='command',
    )
    subparsers.required = True

    generate_parser(subparsers)
    sort_parser(subparsers)

    args = parser.parse_args()
    print(args)

    if args.command == 'generate':
        generate(args.num_lines, args.max_line_length)

    if args.command == 'sort':
        sort(
            args.input_file,
            args.output_file,
            args.sort_max_memory_mb,
            args.merge_max_files,
        )


if __name__ == '__main__':
    main()
