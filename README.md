# forfiles

Utilities for files and images.

## Installation

Add forfiles to a uv project.

```bash
uv add forfiles
```

You can also install forfiles with `pip install --upgrade forfiles`.

## Development

Use uv 0.9.0 or newer to install the locked dependencies and run the project checks.

```bash
uv sync --locked
uv run --locked pytest tests
uv run --locked ruff format --check .
uv run --locked ruff check . --extend-exclude=tests
uv run --locked mypy src/
uv build
```

## Usage

```python
from forfiles import fs, image

# file tools
fs.filter_type('directory-to-filter/', ['.png', '.txt', 'md'])
fs.dir_create('directory-to-create/')
fs.dir_delete('directory-to-delete/')

# image tools
image.scale('boat.png', 1, 1.5)
image.resize('car.jpg', 1000, 1000)
image.to_png('plane.jpg')

# you can also process all files in a directory with a callback function
# arguments after the function are passed to the callback in addition to the file path
fs.process_files('cats/', image.scale, 2, 2)
fs.process_files('giraffes/', image.resize, 1000, 1000)
fs.process_files('tortoises/', image.to_png)

# you can also iterate using a generator syntax
for file in fs.iterate_files('gorillas/'):
    if file.suffix == '.py':
        print(file.name)
```
