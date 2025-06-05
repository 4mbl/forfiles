"""Tools to manipulate images."""

from pathlib import Path
from typing import TypedDict

from PIL import Image

from ._internal import StrOrBytesPath, process_path

DEFAULT_IMAGE_TYPES = (
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


class ImageOptions(TypedDict):
    """Options for image operations."""

    image_types: list[str] | None
    """File extensions containing the leading dot."""


def resize(
    path: StrOrBytesPath, image_width: int, image_height: int, options: ImageOptions | None = None
) -> None:
    """Resize an image or all images in a directory.

    Args:
        path (StrOrBytesPath): path of the image to resize
        image_width (int): width of the desired output image in pixels
        image_height (int): height of the desired output image in pixels
        options (ImageOptions | None): options for resizing

    Returns:
        void

    """
    path = process_path(path) if not isinstance(path, Path) else path

    image_types = (
        options['image_types'] if options and options['image_types'] else DEFAULT_IMAGE_TYPES
    )

    if not path.is_file():
        return

    if path.suffix in (image_types):
        with Image.open(path) as image:
            image.resize(
                (image_width, image_height),
                resample=Image.Resampling.NEAREST,
            ).save(path)


def scale(
    path: StrOrBytesPath,
    width_multiplier: float,
    height_multiplier: float,
    options: ImageOptions | None = None,
) -> None:
    """Scale an image or all images in a directory with the given multipliers.

    Args:
        path (StrOrBytesPath): path of the image to scale or to a directory that contains them
        width_multiplier (float): integer that will be used to multiply the width of the image
        height_multiplier (float): integer that will be used to multiply the width of the image
        options (ImageOptions | None): options for scaling

    Returns:
        void

    """
    path = process_path(path) if not isinstance(path, Path) else path

    image_types = (
        options['image_types'] if options and options['image_types'] else DEFAULT_IMAGE_TYPES
    )

    if not path.is_file():
        return

    if path.suffix in image_types:
        with Image.open(path) as image:
            image_width, image_height = image.size
            image.resize(
                (
                    int(image_width * width_multiplier),
                    int(image_height * height_multiplier),
                ),
                resample=Image.Resampling.NEAREST,
            ).save(path)


def to_png(
    path: StrOrBytesPath,
    options: ImageOptions | None = None,
) -> None:
    """Convert an image file into PNG.

    Args:
        path (StrOrBytesPath): path of the image to convert or to a directory that contains them
        options (ImageOptions | None): options for conversion

    """
    path = process_path(path) if not isinstance(path, Path) else path

    image_types = (
        options['image_types'] if options and options['image_types'] else DEFAULT_IMAGE_TYPES
    )

    if not path.is_file():
        return

    if path.suffix == '.png':
        return
    if path.suffix in image_types:
        with Image.open(path) as image:
            image.save(f'{path.stem}.png')
        path.unlink()
