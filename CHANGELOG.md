# forfiles Changelog

All notable changes to this project will be documented in this file.

---

## Unreleased

### Added

* Add `iterate_files` function to `fs` for iterating over files in a directory with a generator.

### Changed

* BREAKING: Merged `file` and `directory` submodules into a new `fs` submodule.
* BREAKING: Renamed parameters in `fs` to be more consistent.
* BREAKING: Require boolean `blacklist_mode` parameter in `filter_type` to be given as named argument.
* BREAKING: Only support file inputs for image operations. Use `dir_action` to manipulate all files in a directory.
* BREAKING: Rename `dir_action` to `process_files`.

* Allow path-like objects to be passed to path parameters in addition to strings.

### Fixed

### Removed

### Known Issues

---
