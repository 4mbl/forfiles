"""Tools to manipulate images."""

from pathlib import Path

from PIL import Image

from ._internal import StrOrBytesPath, process_path
from .fs import dir_action

IMAGE_TYPES = (
    '.png',
    '.jpg',
    '.gif',
    '.webp',
    '.tiff',
    '.bmp',
    '.jpe',
    '.jfif',
    '.jif',
)


def resize(path: StrOrBytesPath, image_width: int, image_height: int) -> None:
    """Resize an image or all images in a directory.

    Args:
        path (StrOrBytesPath): path of the image to resize or to a directory that contains them
        image_width (int): width of the desired output image in pixels
        image_height (int): height of the desired output image in pixels

    Returns:
        void

    """
    path = process_path(path) if not isinstance(path, Path) else path

    def resize_single(path: Path) -> None:
        if path.suffix in IMAGE_TYPES:
            with Image.open(path) as image:
                image.resize(
                    (image_width, image_height),
                    resample=Image.Resampling.NEAREST,
                ).save(path)

    if path.is_file():
        resize_single(path)

    if path.is_dir():
        dir_action(path, resize_single)


def scale(path: StrOrBytesPath, width_multiplier: float, height_multiplier: float) -> None:
    """Scale an image or all images in a directory with the given multipliers.

    Args:
        path (StrOrBytesPath): path of the image to scale or to a directory that contains them
        width_multiplier (int): integer that will be used to multiply the width of the image
        height_multiplier (int): integer that will be used to multiply the width of the image

    Returns:
        void

    """
    path = process_path(path) if not isinstance(path, Path) else path

    def scale_single(path: Path) -> None:
        if path.suffix in IMAGE_TYPES:
            with Image.open(path) as image:
                image_width, image_height = image.size
                image.resize(
                    (
                        int(image_width * width_multiplier),
                        int(image_height * height_multiplier),
                    ),
                    resample=Image.Resampling.NEAREST,
                ).save(path)

    if path.is_file():
        scale_single(path)

    if path.is_dir():
        dir_action(path, scale_single)


def to_png(path: StrOrBytesPath) -> None:
    """Convert an image file into PNG.

    Args:
        path (StrOrBytesPath): path of the image to convert or to a directory that contains them

    """
    path = process_path(path) if not isinstance(path, Path) else path

    def to_png_single(path: Path) -> None:
        if path.suffix == '.png':
            return
        if path.suffix in IMAGE_TYPES:
            with Image.open(path) as image:
                image.save(f'{path.stem}.png')
            path.unlink()

    if path.is_file():
        to_png_single(path)

    if path.is_dir():
        dir_action(path, to_png_single)
