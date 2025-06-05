from os import PathLike
from typing import Union
from pathlib import Path

StrOrBytesPath = Union[str, bytes, PathLike]
"""Value that can be used as a path, either as a string, bytes or PathLike object."""


def process_path(path: StrOrBytesPath) -> Path:
    """
    Takes a path and converts it to a Path object.
    """
    if isinstance(path, Path):
        return path
    if isinstance(path, bytes):
        path = path.decode("utf-8")
    return Path(path)
