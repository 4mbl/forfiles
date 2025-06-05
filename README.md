# forfiles

forfiles has useful tools for files and images.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install forfiles.

```bash
pip install --upgrade forfiles
```

## Usage

```python
from forfiles import fs, image

# file tools
fs.filter_type("directory-to-filter/", [".png", ".txt", "md"])
fs.dir_create("directory-to-create/")
fs.dir_delete("directory-to-delete/")

# image tools
image.scale("boat.png", 1, 1.5)
image.resize("car.jpg", 1000, 1000)
image.to_png("plane.jpg")

# you can also operate whole directories
fs.dir_action("cats/", image.scale, 2, 2)
fs.dir_action("giraffes/", image.resize, 1000, 1000)
fs.dir_action("tortoises/", image.to_png)
```
