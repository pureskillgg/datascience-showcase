# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## Unreleased

### Added

- A matplotlib style kit, applied on import: PureSkill.gg colors (dark and light), Russo One titles, Assistant text, and the series, side and heat colors.
- Size presets for social posts, slides, link previews and articles, with a `scale` setting for higher resolutions.
- `figure()` for a branded canvas, `legend()` under the subtitle, and `save()`, which adds "Data provided by PureSkill.gg." to every image and stamps PNGs.
- `save_animation()` for MP4s, using the ffmpeg that comes with `imageio-ffmpeg`.
- `load_env()` and `curator()` to find a local tome collection from a `.env` at the repo root.
- Pre-commit and CI checks that keep data, secrets, videos, notebook outputs and unstamped gallery images out of git.

### Changed

- Require Python 3.14 and `pureskillgg-dsdk` 3.2.
- Rewrite the README in Markdown.
- Harden the deploy workflows.
- Update GitHub Actions to Node.js 24 runtimes.

### Removed

- The CS:GO disconnect and M4 notebooks, the notebook template and the old `.env` bootstrap.
- Publishing to PyPI: the publish and version workflows and bump2version. Earlier releases stay on PyPI.

## 0.0.4 / 2026-06-13

### Added

- Disconnect reason analysis notebook.
- M4 usage analysis (June 2022) notebook.

### Changed

- Modernize the GitHub Actions workflows.
- Replace `gr1n/setup-poetry` with `snok/install-poetry` and move caching to `setup-python`.
- Switch the build backend to `poetry-core`.

## 0.0.3 / 2022-06-14

### Fixed

- Fixed the README title underline length.

## 0.0.2 / 2022-06-14

### Changed

- Updated the project description to "Showcase of public PureSkill.gg data set
  applications."

## 0.0.1 / 2022-06-14

### Added

- Initial release of the data science showcase package.
