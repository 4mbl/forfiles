from os import PathLike
from pathlib import Path

StrOrBytesPath = str | bytes | PathLike
"""Value that can be used as a path, either as a string, bytes or PathLike object."""


def process_path(path: StrOrBytesPath) -> Path:
    """Convert a path to a Path object."""
    if isinstance(path, Path):
        return path
    if isinstance(path, bytes):
        path = path.decode('utf-8')
    return Path(path)
