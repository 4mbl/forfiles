from collections.abc import Generator
import pytest
from PIL import Image
from pathlib import Path
import tempfile

import forfiles as image


@pytest.fixture
def temp_dir__image() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def create_test_image(path: Path, size: tuple[int, int] = (100, 100), color: str = 'blue') -> None:
    Image.new('RGB', size, color=color).save(path.as_posix())


def test_resize(temp_dir__image: Path):
    image_path = temp_dir__image / 'image.jpg'
    create_test_image(image_path, size=(200, 200))
    image.resize(image_path, 50, 50)

    with Image.open(image_path) as img:
        assert img.size == (50, 50)


def test_resize_ignores_non_image_file(temp_dir__image: Path):
    non_image = temp_dir__image / 'file.txt'
    non_image.write_text('not an image')
    image.resize(non_image, 10, 10)
    assert non_image.read_text() == 'not an image'


def test_scale(temp_dir__image: Path):
    image_path = temp_dir__image / 'image.jpg'
    create_test_image(image_path, size=(100, 100))
    image.scale(image_path, 2.0, 0.5)

    with Image.open(image_path) as img:
        assert img.size == (200, 50)


def test_to_png(temp_dir__image: Path):
    image_path = temp_dir__image / 'original.jpg'
    create_test_image(image_path)
    image.to_png(image_path)

    png_path = temp_dir__image / 'original.png'
    assert png_path.exists()
    assert not image_path.exists()

    with Image.open(png_path) as img:
        assert img.format == 'PNG'


def test_to_png_skips_png_files(temp_dir__image: Path):
    png_path = temp_dir__image / 'image.png'
    create_test_image(png_path)
    mtime_before = png_path.stat().st_mtime
    image.to_png(png_path)
    mtime_after = png_path.stat().st_mtime
    assert mtime_before == mtime_after
