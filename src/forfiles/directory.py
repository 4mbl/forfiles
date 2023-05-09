import os
from typing import Callable


def dir_action(
    path: str,
    print_paths: bool,
    fn: Callable[..., None],
    *args,
    **kwargs,
) -> None:
    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if print_paths:
                print(file_path.replace("\\", "/"))
            fn(file_path, *args, **kwargs)
