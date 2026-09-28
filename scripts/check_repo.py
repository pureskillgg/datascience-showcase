"""
Keep data, secrets, videos and unstamped images out of the repo.

pre-commit runs this on the files being committed; CI runs it on every tracked
file with --all. Exit 1 lists each problem.

    uv run python scripts/check_repo.py --all
    uv run python scripts/check_repo.py path/to/file ...
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError

STAMP_KEY = "psgg:attribution"
ATTRIBUTION = "Data provided by PureSkill.gg."
MAX_BYTES = 10 * 1024 * 1024
DATA_EXT = {".parquet", ".feather", ".arrow", ".pkl", ".pickle", ".npy", ".npz", ".h5", ".hdf5", ".dem"}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v", ".gif"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".bmp", ".tif", ".tiff"}
PARQUET_MAGIC = b"PAR1"


def notebook_problem(path):
    """A reason the notebook can't be committed, or None."""
    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except ValueError, UnicodeDecodeError:
        return "notebook is not valid JSON"
    for cell in nb.get("cells", []):
        if cell.get("outputs") or cell.get("execution_count") is not None:
            return (
                "notebook has outputs; strip them (pre-commit runs nbstripout, or: uv run nbstripout <file>)"
            )
    return None


def gallery_image_problem(path):
    """A reason the gallery image can't be committed, or None."""
    if path.suffix.lower() != ".png":
        return "gallery images must be PNGs saved with the kit's save()"
    try:
        with Image.open(path) as img:
            text = dict(getattr(img, "text", {}) or {})
    except UnidentifiedImageError, OSError:
        return "not a readable PNG"
    if text.get(STAMP_KEY) != ATTRIBUTION:
        return "gallery image has no kit stamp; save it with pureskillgg_datascience_showcase.save()"
    return None


def file_problems(path, root):
    """Every reason one file can't be committed."""
    rel = path.relative_to(root) if path.is_absolute() else path
    name = path.name
    suffix = path.suffix.lower()
    problems = []
    if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
        problems.append("secrets file; keep your .env out of git (copy .env.example instead)")
    if suffix in DATA_EXT:
        problems.append("data file; data stays out of git")
    if suffix in VIDEO_EXT:
        problems.append("video; publish it on YouTube or similar and commit a still frame and the link")
    if not path.is_file():
        return problems
    size = path.stat().st_size
    if size > MAX_BYTES:
        problems.append(f"{size / 1024 / 1024:.1f} MB is over the {MAX_BYTES // 1024 // 1024} MB limit")
    if suffix not in DATA_EXT:
        with path.open("rb") as fh:
            if fh.read(4) == PARQUET_MAGIC:
                problems.append("parquet data (whatever its name); data stays out of git")
    if suffix == ".ipynb":
        reason = notebook_problem(path)
        if reason:
            problems.append(reason)
    if rel.parts and rel.parts[0] == "gallery" and suffix in IMAGE_EXT:
        reason = gallery_image_problem(path)
        if reason:
            problems.append(reason)
    return problems


def tracked_files(root):
    """Tracked and staged files, from git."""
    out = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True)
    return [Path(p) for p in out.stdout.decode("utf-8").split("\0") if p]


def check(paths, root):
    """Problems for the given paths (relative to root), as 'path: reason' lines."""
    lines = []
    for rel in paths:
        for reason in file_problems(root / rel, root):
            lines.append(f"{rel.as_posix()}: {reason}")
    return lines


def main(argv=None):
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", maxsplit=1)[0])
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--all", action="store_true", help="check every tracked file")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    paths = tracked_files(root) if args.all else [p.resolve().relative_to(root) for p in args.files]
    lines = check(paths, root)
    for line in lines:
        print(line)
    if lines:
        print(f"\n{len(lines)} problem(s). See AGENTS.md for what belongs in this repo.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
