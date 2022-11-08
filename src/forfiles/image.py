import os
from PIL import Image
import layeredimage.io as layered_image
import os


def resize(image_path: str, image_width: int, image_height: int):
    """
    Resizes an image

    Args:
        image_path (string): full path of the image that will be resized
        image_width (int): width of the desired output image in pixels
        image_height (int): height of the desired output image in pixels

    Returns:
        void
    """

    supported_file_types = (
        ".png",
        ".jpg",
        ".gif",
        ".webp",
        ".tiff",
        ".bmp",
        ".jpe",
        ".jfif",
        ".jif",
    )

    if image_path.endswith(supported_file_types):
        with Image.open(image_path) as image:
            image = image.resize(
                (image_width, image_height),
                resample=Image.NEAREST,
            )

            image.save(image_path)


def scale(image_path: str, width_multiplier: float, height_multiplier: float):
    """
    Scales image with the given multiplier(s)

    Args:
        image_path (string): full path of the image that will be resized
        image_width (int): width of the desired output image in pixels
        image_height (int): height of the desired output image in pixels

    Returns:
        void
    """

    SUPPORTED_FILE_TYPES = (".png", ".jpg", ".gif", ".webp", ".tiff", ".bmp")

    if image_path.endswith(SUPPORTED_FILE_TYPES):
        with Image.open(image_path) as image:
            image_width, image_height = image.size

            image = image.resize(
                (int(image_width * width_multiplier),
                 int(image_height * height_multiplier)),
                resample=Image.Resampling.NEAREST,
            )

            image.save(image_path)


def dir_scale(dir_path: str, width_multiplier: float, height_multiplier: float):
    """
    Scales every image in a directory and its sub directories.

    Args:
        dir_path (str): path of the directory that will be used
        width_multiplier (int): width of all images is multiplied by this
        height_multiplier (int): height of all images is multiplied by this
    """

    for root, subdirs, files in os.walk(dir_path):
        for file in files:
            print(os.path.join(root, file).replace("\\", "/"))
            scale(os.path.join(root, file), width_multiplier, height_multiplier)


def dir_resize(dir_path: str, image_width: int, image_height: int):
    """
    Resizes every image in a directory and its sub directories.

    Args:
        dir_path (str): path of the directory that will be used
        width_multiplier (int): width of the desired output image in pixels
        height_multiplier (int): height of the desired output image in pixels
    """

    for root, subdirs, files in os.walk(dir_path):
        for file in files:
            print(os.path.join(root, file).replace("\\", "/"))
            resize(os.path.join(root, file), image_width, image_height)


def to_png(path: str):
    """Converts normal image or layered image file into PNG.

    Args:
        image_path (str): path of the layered image to convert
    """

    LAYERED_IMAGE_TYPES = (".ora", ".pdn", ".xcf", ".psd", ".tiff", ".tif",
                           ".webp", ".gif", ".lsr")
    IMAGE_TYPES = (".png", ".jpg", ".gif", ".webp", ".tiff", ".bmp", ".jpe",
                   ".jfif", ".jif")

    filename = os.path.splitext(path)[0]

    if (path.endswith(LAYERED_IMAGE_TYPES)):
        image = layered_image.openLayerImage(path)
        image.getFlattenLayers().save(f"{filename}.png")
    if (path.endswith(IMAGE_TYPES)):
        image = Image.open(path)
        image.save(f"{filename}.png")

    os.remove(path)


if __name__ == "__main__":
    home_dir = os.path.expanduser('~')

    resize(f"{home_dir}/Downloads/goat.jpg", 1600, 1600)
    scale(f"{home_dir}/Downloads/fox.png", 2.5, 3.3)
    dir_scale(f"{home_dir}/Downloads/cats", 2, 2)
    dir_resize(f"{home_dir}/Downloads/giraffes", 44, 66)
    to_png(f"{home_dir}/Downloads/parrot.xcf")
    to_png(f"{home_dir}/Downloads/chicken.jpg")
