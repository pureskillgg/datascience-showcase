# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## Unreleased

## 0.0.4 / 2026-06-13

### Added

- Disconnect reason analysis notebook.
- M4 usage analysis (June 2022) notebook.

### Changed

- Modernized GitHub Actions workflows so current runners can schedule them:
  `ubuntu-20.04` runners to `ubuntu-latest`, `actions/checkout` v2 to v5,
  `actions/setup-python` v3 to v6, `crazy-max/ghaction-import-gpg` v4 to v7,
  and `stefanzweifel/git-auto-commit-action` v4 to v7.
- Replaced the abandoned `gr1n/setup-poetry` action with the maintained
  `snok/install-poetry@v1` (Poetry 1.2.1) and moved dependency caching to
  `actions/setup-python`'s built-in `cache: poetry`.
- Switched the build backend to `poetry-core` (`poetry.core.masonry.api`) so
  source distributions use PEP 625-compliant filenames on PyPI.

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
