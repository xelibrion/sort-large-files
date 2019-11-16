import argparse

from external_sort.generate import generate


def main():
    parser = argparse.ArgumentParser(description="Sort large files")
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

    args = parser.parse_args()
    print(args)

    generate(args.num_lines, args.max_line_length)


if __name__ == '__main__':
    main()
