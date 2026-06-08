#!/usr/bin/env python3
"""Convert course materials to Markdown with Microsoft MarkItDown."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import warnings
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path.home() / ".pass-all-exams" / "courses"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "course"


def course_dir(course: str, root: Path = ROOT) -> Path:
    return root / slugify(course)


def read_json(path: Path, fallback):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def iter_jsonl(path: Path):
    if not path.exists():
        return iter(())
    return (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def append_jsonl(path: Path, item) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(item, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_name(path: Path, digest: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff._-]+", "-", path.stem).strip("-")
    return f"{stem or 'material'}-{digest[:10]}.md"


def import_markitdown():
    warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv.*", category=RuntimeWarning)
    try:
        from markitdown import MarkItDown
        from markitdown import MarkItDownException

        return MarkItDown, MarkItDownException
    except ModuleNotFoundError as exc:
        print(
            "MarkItDown is not installed. Install it with:\n"
            "  python3 -m pip install 'markitdown[all]'\n"
            "or use:\n"
            "  python3 -m pip install -r requirements-markitdown.txt",
            file=sys.stderr,
        )
        raise SystemExit(2) from exc


def build_markdown_header(record: dict) -> str:
    lines = [
        "<!-- pass-all-exams material",
        f"source: {record['source']}",
        f"sha256: {record['sha256']}",
        f"converted_at: {record['converted_at']}",
        "converter: microsoft/markitdown",
        "-->",
        "",
    ]
    return "\n".join(lines)


def convert_one(args, source: str, markitdown) -> dict:
    parsed = urlparse(source)
    if parsed.scheme in {"http", "https"} and not args.allow_url:
        raise ValueError(f"URL input is disabled by default: {source}. Re-run with --allow-url if this is trusted.")
    if parsed.scheme and parsed.scheme not in {"", "file", "http", "https"}:
        raise ValueError(f"Unsupported source scheme: {parsed.scheme}")

    if parsed.scheme in {"http", "https"}:
        source_id = source
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
        display_name = Path(parsed.path).name or parsed.netloc or "url"
        output_name = safe_name(Path(display_name), digest)
    else:
        path = Path(source).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(path)
        if not path.is_file():
            raise ValueError(f"Not a file: {path}")
        source_id = str(path)
        digest = sha256_file(path)
        output_name = safe_name(path, digest)

    course_path = course_dir(args.course, args.root)
    ensure_course_state(course_path, args.course)
    materials_dir = course_path / "materials"
    materials_dir.mkdir(parents=True, exist_ok=True)
    index_path = course_path / "materials.jsonl"
    output_path = materials_dir / output_name

    previous = [item for item in iter_jsonl(index_path) if item.get("sha256") == digest and item.get("output")]
    if previous and output_path.exists() and not args.force:
        return {**previous[-1], "status": "cached"}

    result = markitdown.convert(source_id, keep_data_uris=args.keep_data_uris)
    markdown = result.text_content
    if not markdown.strip():
        raise ValueError(f"Conversion produced empty Markdown: {source}")

    record = {
        "date": dt.date.today().isoformat(),
        "converted_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "course": args.course,
        "source": source_id,
        "sha256": digest,
        "output": str(output_path),
        "title": getattr(result, "title", None),
        "bytes": len(markdown.encode("utf-8")),
        "status": "converted",
    }
    output_path.write_text(build_markdown_header(record) + markdown.rstrip() + "\n", encoding="utf-8")
    append_jsonl(index_path, record)
    update_state(course_path)
    return record


def ensure_course_state(course_path: Path, course: str) -> None:
    course_path.mkdir(parents=True, exist_ok=True)
    state_path = course_path / "state.json"
    if not state_path.exists():
        today = dt.date.today().isoformat()
        write_json(
            state_path,
            {
                "course": course,
                "slug": course_path.name,
                "created_at": today,
                "updated_at": today,
                "mode": "compact",
                "stage": "intake",
                "counts": {
                    "points_total": 0,
                    "points_done": 0,
                    "errors": 0,
                    "stubborn": 0,
                    "cards": 0,
                    "materials": 0,
                },
                "points": {},
            },
        )
    config_path = course_path / "course.yaml"
    if not config_path.exists():
        config_path.write_text(
            f"course: {course}\nmode: compact\n\nmust_know: []\nkey_points: []\nexam_types: []\nmaterials: {{}}\n",
            encoding="utf-8",
        )


def update_state(course_path: Path) -> None:
    state_path = course_path / "state.json"
    state = read_json(state_path, {})
    records = list(iter_jsonl(course_path / "materials.jsonl"))
    counts = state.setdefault("counts", {})
    counts["materials"] = len({item.get("sha256") for item in records if item.get("sha256")})
    state["updated_at"] = dt.date.today().isoformat()
    write_json(state_path, state)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert uploaded course materials to Markdown with MarkItDown.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--course", required=True)
    parser.add_argument("--force", action="store_true", help="Re-convert even if a material with the same hash exists.")
    parser.add_argument("--allow-url", action="store_true", help="Allow trusted http(s) sources. Local files are safer and preferred.")
    parser.add_argument("--use-plugins", action="store_true", help="Enable installed MarkItDown plugins.")
    parser.add_argument("--keep-data-uris", action="store_true", help="Keep embedded data URIs in Markdown output.")
    parser.add_argument("sources", nargs="+", help="Local file paths by default; trusted URLs require --allow-url.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    MarkItDown, MarkItDownException = import_markitdown()
    markitdown = MarkItDown(enable_plugins=args.use_plugins)

    converted = []
    for source in args.sources:
        try:
            converted.append(convert_one(args, source, markitdown))
        except (OSError, ValueError, MarkItDownException) as exc:
            print(json.dumps({"source": source, "status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
            raise SystemExit(1) from exc

    print(json.dumps(converted, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
