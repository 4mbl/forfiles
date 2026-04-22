# forfiles Changelog

All notable changes to this project will be documented in this file.

---

<!-- ## Unreleased -->

## 6.0.0 | 2026-04-22

- Add support for Python 3.14.

### Added

- Add `iterate_files` function to `fs` for iterating over files in a directory with a generator.

### Changed

- BREAKING: Merged `file` and `directory` submodules into a new `fs` submodule.
- BREAKING: Renamed parameters in `fs` to be more consistent.
- BREAKING: Require boolean `blacklist_mode` parameter in `filter_type` to be given as named argument.
- BREAKING: Rename `dir_action` to `process_files`.
- BREAKING: Only support file inputs for image operations. Use `process_files` to manipulate all files in a directory.

- Allow path-like objects to be passed to path parameters in addition to strings.
- Allow other Sequence types to be passed to some functions in addition to lists on some functions.
- Allow image types to be overriden in `resize`, `scale`, `to_png`

### Fixed

### Removed

### Known Issues

---
