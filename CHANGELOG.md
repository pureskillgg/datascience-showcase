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
- `load_env()`, `curator()` and `list_tomes()` to find a local tome collection from a `.env` at the repo root.
- Pre-commit and CI checks that keep data, secrets, videos, notebook outputs and unstamped gallery images out of git.
- Stock radars and Valve's overview numbers for 14 maps, with `maps.draw_radar()`, `to_radar()`, `level_of()`, `heatmap()` and `label_sites()`.
- Docs: getting the data, a data primer with field notes, and a style guide with images rendered by the kit.
- AGENTS.md and a `make-graphic` skill for coding agents.
- A gallery with an index built from each item's README, a gallery item template, and CONTRIBUTING.md.

### Changed

- Pin workflow runners to `ubuntu-24.04`.
- Require Python 3.14 and `pureskillgg-dsdk` 4. Its `build_basic_tomes` builds tomes that mix older and newer matches; `make_tome` still fails on a page that mixes their flag columns.
- `docs/getting-data.md` and the `make-graphic` skill build tomes with `build_basic_tomes`, and keep `make_tome` for summarizing each match first, with the flag pitfall and its fix.
- Rewrite the README in Markdown.

### Removed

- The CS:GO disconnect and M4 notebooks, the notebook template and the old `.env` bootstrap.
- Publishing to PyPI: the publish and version workflows and bump2version. Earlier releases stay on PyPI.

## 0.0.8 / 2026-09-22

### Changed

- Publish to PyPI with `uv publish` instead of `twine`.

### Fixed

- Publish workflow failing on `import twine` (`KeyError: 'license'`).

## 0.0.6 / 2026-08-27

### Changed

- Harden the deploy workflows.

## 0.0.5 / 2026-08-24

### Changed

- Update GitHub Actions to Node.js 24 runtimes.

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
