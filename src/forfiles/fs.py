import os
from shutil import rmtree
from typing import Callable


def filter_type(directory: str, file_types: list, blacklist_mode: bool = False):
    """
    Filters files in a directory based on their file type

    Args:
        directory (string): full path to the directory where the files will be filtered
        desired_file_types (list): file type extensions that will be kept, for example: [".png", ".txt"]
        blacklist_mode (bool): by default the listed file types are kept, if this is set to true, the listed file types will be removed and other remaining files will be kept

    Returns:
        void
    """

    for file_type in file_types:
        if not file_type.startswith("."):
            file_type = f".{file_type}"

    for subdir, _, files in os.walk(directory):
        for file in files:
            if blacklist_mode and file.endswith(tuple(file_types)):
                os.remove(f"{os.path.abspath(subdir)}/{file}")
            elif not file.endswith(tuple(file_types)):
                os.remove(f"{os.path.abspath(subdir)}/{file}")


def dir_create(dir_path: str):
    """Creates directory is it does not exist previously

    Args:
        dir_path (str): path of the directory that will be created
    """
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def dir_delete(dir_path: str):
    """Deletes directory and its contents if it exists.

    Args:
        dir_path (string): path of the directory that will be deleted
    """
    if os.path.isdir(dir_path):
        rmtree(dir_path)


def dir_action(
    path: str,
    fn: Callable[..., None],
    *args,
    **kwargs,
) -> None:
    """Iterates through a directory and executes a function for each file in the directory.

    Args:
        path (str):
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

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            fn(file_path, *args, **kwargs)
