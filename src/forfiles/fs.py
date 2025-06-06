"""Tools for the filesystem."""

import os
from collections.abc import Callable, Generator
from pathlib import Path
from shutil import rmtree
from typing import Concatenate, ParamSpec

from forfiles._internal import StrOrBytesPath, process_path


def filter_type(
    directory: StrOrBytesPath, file_types: list, *, blacklist_mode: bool = False
) -> None:
    """Filter files in a directory based on their file type.

    Args:
        directory (StrOrBytesPath):
            Path to the directory to be filtered.
        file_types (list):
            File type extensions that will be kept, for example: `[".png", ".txt"]`
        blacklist_mode (bool):
            When true, listed types will be removed, otherwise they will be kept.

    """
    directory = process_path(directory) if not isinstance(directory, Path) else directory
    file_types = [
        f'.{file_type}' if not file_type.startswith('.') else file_type for file_type in file_types
    ]

    for subdir, _, files in os.walk(directory.as_posix()):
        for file in files:
            if (blacklist_mode and file.endswith(tuple(file_types))) or not file.endswith(
                tuple(file_types)
            ):
                file_path = Path(subdir) / file
                if file_path.is_file():
                    file_path.unlink()


def dir_create(directory: StrOrBytesPath) -> None:
    """Create directory is it does not exist previously. Will create parents.

    Args:
        directory (StrOrBytesPath):
            Path of the directory that will be created.

    """
    directory = process_path(directory) if not isinstance(directory, Path) else directory
    if not directory.is_dir():
        directory.mkdir(parents=True, exist_ok=True)


def dir_delete(directory: StrOrBytesPath) -> None:
    """Delete directory and its contents if it exists.

    Args:
        directory (StrOrBytesPath): path of the directory that will be deleted

    """
    directory = process_path(directory) if not isinstance(directory, Path) else directory
    if directory.is_dir():
        rmtree(directory)


P = ParamSpec('P')


def process_files(
    directory: StrOrBytesPath,
    fn: Callable[Concatenate[Path, P], None],
    *args: P.args,
    **kwargs: P.kwargs,
) -> None:
    """Iterate through a directory and execute a function for each file in the directory.

    You can use `iterate_files` if you prefer to iterate through files with a generator.

    Args:
        directory (StrOrBytesPath):
            Path of the directory to iterate through.

        fn (Callable):
            Callback function that will be called with each file as its argument.

        *args:
            Optional positional arguments that will be passed to the callback function.

        **kwargs:
            Optional keyword arguments that will be passed to the callback function.

    Examples:
        The following code demonstrates how to print the contents of a directory:

        >>> def print_contents(file_path):
        ...     with open(file_path, 'r') as file:
        ...         print(file.read())

        >>> process_files('/path/to/directory', print_contents)

    """
    directory = process_path(directory) if not isinstance(directory, Path) else directory
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            fn(file_path, *args, **kwargs)


def iterate_files(directory: StrOrBytesPath) -> Generator[Path, None, None]:
    """Iterate through a directory and yield the paths of each file.

    You can use `process_files` if you prefer to process files with a callback function.

    Args:
        directory (StrOrBytesPath):
            Path of the directory to iterate through.

    Yields:
        Path:
            The path of each file in the directory.

    Examples:
        The following code demonstrates how to print the paths of all files:

        >>> for file in iterate_files('/path/to/directory'):
        >>>     print(file)

    """
    directory = process_path(directory) if not isinstance(directory, Path) else directory
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            yield file_path
