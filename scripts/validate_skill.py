#!/usr/bin/env python3
"""Validate the portable skill package."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        fail("frontmatter is not closed")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def main() -> None:
    skill = ROOT / "SKILL.md"
    if not skill.exists():
        fail("missing SKILL.md")
    meta = frontmatter(skill.read_text(encoding="utf-8"))
    name = meta.get("name")
    description = meta.get("description", "")
    if not name:
        fail("missing name")
    if not NAME_RE.match(name):
        fail(f"invalid skill name: {name}")
    if len(name) > 64:
        fail("skill name longer than 64 chars")
    if not description:
        fail("missing description")
    if len(description) > 1024:
        fail("description longer than 1024 chars")

    required = [
        "references/pipeline.md",
        "references/prompt-patterns.md",
        "references/platforms.md",
        "scripts/examctl.py",
        "scripts/install.sh",
        "scripts/package_skill.py",
        "agents/openai.yaml",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            fail(f"missing {rel}")

    print("OK: pass-all-exams skill package is valid")


if __name__ == "__main__":
    main()
