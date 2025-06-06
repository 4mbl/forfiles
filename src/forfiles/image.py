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
    """Resize an image.

    Args:
        path (StrOrBytesPath):
            Path of the image to resize.
        image_width (int):
            Width of the desired output image in pixels.
        image_height (int):
            Height of the desired output image in pixels
        options (ImageOptions | None):
            Options for resizing.

    """
    path = process_path(path)

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
    """Scale an image with the given multipliers.

    Args:
        path (StrOrBytesPath):
            Path of the image to scale.
        width_multiplier (float):
            Integer that will be used to multiply the width of the image.
        height_multiplier (float):
            Integer that will be used to multiply the width of the image.
        options (ImageOptions | None):
            Options for scaling

    """
    path = process_path(path)

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
) -> Path | None:
    """Convert an image file into PNG.

    Args:
        path (StrOrBytesPath):
            Path of the image to convert.
        options (ImageOptions | None):
            Options for conversion.

    Returns:
        Path | None: The path of the converted image, or None if conversion was not possible.

    """
    path = process_path(path)

    image_types = (
        options['image_types'] if options and options['image_types'] else DEFAULT_IMAGE_TYPES
    )

    if not path.is_file():
        return None
    if path.suffix not in image_types:
        return None
    if path.suffix == '.png':
        return path

    with Image.open(path) as image:
        new_path = path.with_suffix('.png')
        image.save(new_path, format='PNG')
    path.unlink()
    return new_path
