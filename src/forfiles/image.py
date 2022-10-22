import os
from PIL import Image  # py -m pip install Pillow


def resize(image_path: str, image_width: int, image_height: int):
    """
    Resizes an image

    Parameters:
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
            # image_width, image_height = image.size

            image = image.resize(
                (image_width, image_height),
                resample=Image.NEAREST,
            )

            image.save(image_path)


def scale(image_path, width_multiplier, height_multiplier):
    """
    Scales image with the given multiplier(s)

    Parameters:
        image_path (string): full path of the image that will be resized
        image_width (int): width of the desired output image in pixels
        image_height (int): height of the desired output image in pixels

    Returns:
        void
    """

    supported_file_types = (".png", ".jpg", ".gif", ".webp", ".tiff", ".bmp")

    if image_path.endswith(supported_file_types):
        with Image.open(image_path) as image:
            image_width, image_height = image.size

            image = image.resize(
                (image_width * width_multiplier, image_height * height_multiplier),
                resample=Image.Resampling.NEAREST,
            )

            image.save(image_path)


def scale_dir(dir_path: str, width_multiplier: int, height_multiplier: int):
    """
    Scales every image in a directory and its sub directories.

    Args:
        dir_path (str): path of the directory that will be used
        width_multiplier (int): width of all images is multiplied by this
        height_multiplier (int): height of all images is multiplied by this
    """
    for root, subdirs, files in os.walk(dir_path):
        for file in files:
            print(os.path.join(root, file))
            scale(os.path.join(root, file),  width_multiplier, height_multiplier)


def resize_dir(dir_path: str, image_width: int, image_height: int):
    """
    Resizes every image in a directory and its sub directories.

    Args:
        dir_path (str): path of the directory that will be used
        width_multiplier (int): width of the desired output image in pixels
        height_multiplier (int): height of the desired output image in pixels
    """
    for root, subdirs, files in os.walk(dir_path):
        for file in files:
            print(os.path.join(root, file))
            resize(os.path.join(root, file),  image_width, image_height)


if __name__ == "__main__":
    resize("C:/Users/User1/Downloads/car.jpg", 1600, 1600)
    scale("C:/Users/User1/Downloads/car.jpg", 10, 10)
    scale_dir("C:/Users/User1/Downloads/cats", 2, 2)
    resize_dir("C:/Users/User1/Downloads/giraffes", 44, 66)
