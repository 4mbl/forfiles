"""Tools for the filesystem."""

import os
from collections.abc import Callable
from pathlib import Path
from shutil import rmtree
from typing import Concatenate, ParamSpec

from forfiles._internal import StrOrBytesPath, process_path


def filter_type(
    directory: StrOrBytesPath, file_types: list, *, blacklist_mode: bool = False
) -> None:
    """Filter files in a directory based on their file type.

    Args:
        directory (StrOrBytesPath): full path to the directory where the files will be filtered
        file_types (list): file type extensions that will be kept, for example: `[".png", ".txt"]`
        blacklist_mode (bool): when true, listed types will be removed, otherwise they will be kept

    Returns:
        void

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
        directory (StrOrBytesPath): path of the directory that will be created

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


def dir_action(
    directory: StrOrBytesPath,
    fn: Callable[Concatenate[Path, P], None],
    *args: P.args,
    **kwargs: P.kwargs,
) -> None:
    """Iterate through a directory and executes a function for each file in the directory.

    Args:
        directory (StrOrBytesPath):
            The path of the directory to iterate through.

        fn (Callable):
            A callback function that will be called with each file as its argument.

        *args:
            Optional positional arguments that will be passed to the callback function.

        **kwargs:
            Optional keyword arguments that will be passed to the callback function.

    Returns:
        None. This function does not return any value.

    Raises:
        OSError: If the directory specified by 'path' does not exist or cannot be accessed.

    Examples:
        The following code demonstrates how to use dir_action to print the contents of a directory:

        >>> def print_file_contents(file_path):
        ...     with open(file_path, 'r') as file:
        ...         print(file.read())

        >>> dir_action('/path/to/directory', print_file_contents)

        The example prints the contents of each file in the specified directory.

    """
    directory = process_path(directory) if not isinstance(directory, Path) else directory
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            fn(file_path, *args, **kwargs)
