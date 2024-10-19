"""Script for formatting multiple Python files.

The formatting is done in-place. If formatting doesn't change the
contents of the file, the file will not be overwritten.
"""
import argparse
import sys
from pathlib import Path
from typing import List

from .formatter import format_text


def format_file(file_path: Path) -> None:
    """In-place formats python source file.

    If the formatting does not change the contents of the file, the file will not be overwritten.

    Args:
        file_path: Path to the file to format.
    """
    try:
        with open(file_path, 'r') as fd:
            file_text = fd.read()

        formatted_file_text = format_text(file_text)

        if formatted_file_text != file_text:
            with open(file_path, 'w') as fd:
                fd.write(formatted_file_text)
    except Exception as error:
        print(f'Cannot format {file_path}: {error}')


def format_files(file_paths: List[Path]) -> None:
    """In-place formats multiple files.

    Args:
        file_paths: Paths to files to format.
    """
    for file_path in file_paths:
        format_file(file_path)


def main() -> int:
    """Script entry point.

    Returns:
        Exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__, prog='py-consistent-formatter')
    parser.add_argument(
        'python_files',
        metavar='python-file',
        nargs='+',
        type=Path,
        help='Path to file to format',
    )
    args = parser.parse_args()

    format_files(args.python_files)

    return 0


if __name__ == '__main__':
    sys.exit(main())
