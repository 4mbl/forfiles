from collections.abc import Generator
import pytest
import tempfile
from pathlib import Path

from forfiles import fs


@pytest.fixture
def temp_dir__fs() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_dir_create(temp_dir__fs: Path):
    new_dir = temp_dir__fs / 'nested/dir'
    assert not new_dir.exists()
    fs.dir_create(new_dir)
    assert new_dir.is_dir()


def test_dir_delete(temp_dir__fs: Path):
    target = temp_dir__fs / 'to_delete'
    fs.dir_create(target / 'nested')
    (target / 'file1.txt').write_text('file1')
    (target / 'nested' / 'file2.txt').write_text('file2')

    assert target.exists()
    assert (target / 'file1.txt').exists()
    assert (target / 'nested' / 'file2.txt').exists()

    fs.dir_delete(target)

    assert not target.exists()
    assert not (target / 'file1.txt').exists()
    assert not (target / 'nested').exists()


def test_filter_type(temp_dir__fs: Path):
    keep = temp_dir__fs / 'keep.txt'
    remove = temp_dir__fs / 'remove.jpg'
    keep.write_text('text')
    remove.write_text('image')
    fs.filter_type(temp_dir__fs, ['.txt'])
    assert keep.exists()
    assert not remove.exists()


def test_filter_type_whitelist(temp_dir__fs: Path):
    keep = temp_dir__fs / 'keep.txt'
    remove = temp_dir__fs / 'remove.jpg'
    keep.write_text('text')
    remove.write_text('image')
    fs.filter_type(temp_dir__fs, ['.txt'], blacklist_mode=False)
    assert keep.exists()
    assert not remove.exists()


def test_filter_type_blacklist(temp_dir__fs: Path):
    keep = temp_dir__fs / 'keep.txt'
    remove = temp_dir__fs / 'remove.jpg'
    keep.write_text('text')
    remove.write_text('image')
    fs.filter_type(temp_dir__fs, ['.jpg'], blacklist_mode=True)
    assert keep.exists()
    assert not remove.exists()


def test_process_files(temp_dir__fs: Path):
    (temp_dir__fs / 'file1.txt').write_text('1')
    (temp_dir__fs / 'file2.txt').write_text('2')
    visited = []

    def visitor(path: Path, suffix: str):
        visited.append(path.name + suffix)

    fs.process_files(temp_dir__fs, visitor, '-suffix')
    assert sorted(visited) == ['file1.txt-suffix', 'file2.txt-suffix']


def test_iterate_files(temp_dir__fs: Path):
    files = [temp_dir__fs / f'file{i}.txt' for i in range(3)]
    for file in files:
        file.write_text('content')

    listed_files = list(fs.iterate_files(temp_dir__fs))
    assert sorted(p.name for p in listed_files) == sorted(f.name for f in files)
