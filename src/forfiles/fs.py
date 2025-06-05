import os
from pathlib import Path
from shutil import rmtree
from typing import Callable

from forfiles._internal import StrOrBytesPath, process_path


def filter_type(
    directory: StrOrBytesPath, file_types: list, *, blacklist_mode: bool = False
):
    """
    Filters files in a directory based on their file type

    Args:
        directory (StrOrBytesPath): full path to the directory where the files will be filtered
        desired_file_types (list): file type extensions that will be kept, for example: [".png", ".txt"]
        blacklist_mode (bool): by default the listed file types are kept, if this is set to true, the listed file types will be removed and other remaining files will be kept

    Returns:
        void
    """
    directory = (
        process_path(directory) if not isinstance(directory, Path) else directory
    )

    for file_type in file_types:
        if not file_type.startswith("."):
            file_type = f".{file_type}"

    for subdir, _, files in os.walk(directory.as_posix()):
        for file in files:
            if blacklist_mode and file.endswith(tuple(file_types)):
                os.remove(f"{os.path.abspath(subdir)}/{file}")
            elif not file.endswith(tuple(file_types)):
                os.remove(f"{os.path.abspath(subdir)}/{file}")


def dir_create(directory: StrOrBytesPath):
    """Creates directory is it does not exist previously. Will create parent directories if they do not exist.

    Args:
        directory (StrOrBytesPath): path of the directory that will be created
    """
    directory = (
        process_path(directory) if not isinstance(directory, Path) else directory
    )
    if not directory.is_dir():
        directory.mkdir(parents=True, exist_ok=True)


def dir_delete(directory: StrOrBytesPath):
    """Deletes directory and its contents if it exists.

    Args:
        directory (StrOrBytesPath): path of the directory that will be deleted
    """
    directory = (
        process_path(directory) if not isinstance(directory, Path) else directory
    )
    if directory.is_dir():
        rmtree(directory)


def dir_action(
    directory: StrOrBytesPath,
    fn: Callable[..., None],
    *args,
    **kwargs,
) -> None:
    """Iterates through a directory and executes a function for each file in the directory.

    Args:
        directory (StrOrBytesPath):
            The path of the directory to iterate through.

        fn (Callable[..., None]):
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

        This will print the contents of each file in the directory '/path/to/directory', as well as its path.
    """
    directory = (
        process_path(directory) if not isinstance(directory, Path) else directory
    )
    for file_path in directory.rglob("*"):
        if file_path.is_file():
            fn(file_path, *args, **kwargs)
