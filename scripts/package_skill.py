#!/usr/bin/env python3
"""Build a .skill zip package for upload-capable agents."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXCLUDES = {
    ".git",
    ".DS_Store",
    "__pycache__",
    ".pass-all-exams",
    "dist",
}


def should_skip(path: Path) -> bool:
    parts = set(path.relative_to(ROOT).parts)
    if parts & DEFAULT_EXCLUDES:
        return True
    return path.suffix in {".pyc", ".pyo"}


def build(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob("*")):
            if path.is_dir() or should_skip(path):
                continue
            archive.write(path, Path("pass-all-exams") / path.relative_to(ROOT))
    print(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Package pass-all-exams as a .skill zip.")
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "pass-all-exams.skill")
    args = parser.parse_args()
    build(args.output)


if __name__ == "__main__":
    main()
