#!/usr/bin/env python3
"""Deterministic state helper for pass-all-exams."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


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


def append_jsonl(path: Path, item) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(item, ensure_ascii=False) + "\n")


def iter_jsonl(path: Path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            yield json.loads(line)


def ensure_course(course: str, root: Path = ROOT) -> Path:
    path = course_dir(course, root)
    path.mkdir(parents=True, exist_ok=True)
    return path


def cmd_init(args) -> None:
    path = ensure_course(args.course, args.root)
    state_path = path / "state.json"
    if state_path.exists() and not args.force:
        print(f"exists: {path}")
        return

    today = dt.date.today().isoformat()
    state = {
        "course": args.course,
        "slug": path.name,
        "created_at": today,
        "updated_at": today,
        "mode": args.mode,
        "stage": "intake",
        "counts": {
            "points_total": 0,
            "points_done": 0,
            "errors": 0,
            "stubborn": 0,
            "cards": 0,
        },
        "points": {},
    }
    write_json(state_path, state)
    for name in ("cards.jsonl", "errors.jsonl", "sessions.jsonl"):
        (path / name).touch(exist_ok=True)
    config = path / "course.yaml"
    if not config.exists():
        config.write_text(
            f"course: {args.course}\nmode: {args.mode}\n\nmust_know: []\nkey_points: []\nexam_types: []\nmaterials: {{}}\n",
            encoding="utf-8",
        )
    print(path)


def cmd_record_point(args) -> None:
    path = ensure_course(args.course, args.root)
    state_path = path / "state.json"
    state = read_json(state_path, {})
    today = dt.date.today().isoformat()
    points = state.setdefault("points", {})
    current = points.get(args.point, {})
    current.update(
        {
            "level": args.level,
            "status": args.status,
            "source": args.source,
            "updated_at": today,
        }
    )
    points[args.point] = current
    state["updated_at"] = today
    state.setdefault("counts", {})
    state["counts"]["points_total"] = len(points)
    state["counts"]["points_done"] = sum(1 for item in points.values() if item.get("status") in {"taught", "corrected", "mastered"})
    write_json(state_path, state)
    print(json.dumps(current, ensure_ascii=False))


def cmd_record_error(args) -> None:
    path = ensure_course(args.course, args.root)
    item = {
        "date": dt.date.today().isoformat(),
        "point": args.point,
        "reason": args.reason,
        "question_type": args.question_type,
        "must_know": args.must_know,
        "status": "stubborn" if args.stubborn else "open",
    }
    append_jsonl(path / "errors.jsonl", item)
    state_path = path / "state.json"
    state = read_json(state_path, {})
    errors = list(iter_jsonl(path / "errors.jsonl") or [])
    state.setdefault("counts", {})
    state["counts"]["errors"] = len(errors)
    state["counts"]["stubborn"] = sum(1 for error in errors if error.get("status") == "stubborn")
    state["updated_at"] = dt.date.today().isoformat()
    write_json(state_path, state)
    print(json.dumps(item, ensure_ascii=False))


def cmd_add_card(args) -> None:
    path = ensure_course(args.course, args.root)
    item = {
        "date": dt.date.today().isoformat(),
        "point": args.point,
        "front": args.front,
        "back": args.back,
        "due": args.due,
        "priority": args.priority,
    }
    append_jsonl(path / "cards.jsonl", item)
    state_path = path / "state.json"
    state = read_json(state_path, {})
    cards = list(iter_jsonl(path / "cards.jsonl") or [])
    state.setdefault("counts", {})
    state["counts"]["cards"] = len(cards)
    state["updated_at"] = dt.date.today().isoformat()
    write_json(state_path, state)
    print(json.dumps(item, ensure_ascii=False))


def cmd_status(args) -> None:
    path = course_dir(args.course, args.root)
    state = read_json(path / "state.json", {})
    errors = list(iter_jsonl(path / "errors.jsonl") or [])
    cards = list(iter_jsonl(path / "cards.jsonl") or [])
    result = {
        "course": state.get("course", args.course),
        "stage": state.get("stage", "unknown"),
        "mode": state.get("mode", "compact"),
        "counts": state.get("counts", {}),
        "open_errors": [item for item in errors if item.get("status") == "open"][-10:],
        "due_cards": [item for item in cards if item.get("due", "") <= dt.date.today().isoformat()][:10],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_summary(args) -> None:
    path = course_dir(args.course, args.root)
    state = read_json(path / "state.json", {})
    points = state.get("points", {})
    errors = list(iter_jsonl(path / "errors.jsonl") or [])
    stubborn = [item for item in errors if item.get("status") == "stubborn"]
    must = {name: data for name, data in points.items() if data.get("level") == "must"}
    print(f"# {state.get('course', args.course)} 复习摘要")
    print()
    print(f"- 阶段: {state.get('stage', 'unknown')}")
    print(f"- 已记录知识点: {len(points)}")
    print(f"- 错题记录: {len(errors)}")
    print(f"- 顽固点: {len(stubborn)}")
    if must:
        print("\n## Must-know 状态")
        for name, data in must.items():
            print(f"- {name}: {data.get('status', 'unknown')}")
    if stubborn:
        print("\n## 顽固点")
        for item in stubborn:
            print(f"- {item.get('point')} ({item.get('reason')})")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage pass-all-exams course state.")
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--course", required=True)
    init.add_argument("--mode", choices=["compact", "standard", "deep"], default="compact")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    point = sub.add_parser("record-point")
    point.add_argument("--course", required=True)
    point.add_argument("--point", required=True)
    point.add_argument("--level", choices=["must", "key", "support"], default="key")
    point.add_argument("--status", choices=["mapped", "taught", "tested", "corrected", "mastered", "stubborn"], default="mapped")
    point.add_argument("--source", choices=["material", "inferred", "needs-confirmation"], default="needs-confirmation")
    point.set_defaults(func=cmd_record_point)

    error = sub.add_parser("record-error")
    error.add_argument("--course", required=True)
    error.add_argument("--point", required=True)
    error.add_argument("--reason", required=True)
    error.add_argument("--question-type", default="unknown")
    error.add_argument("--must-know", action="store_true")
    error.add_argument("--stubborn", action="store_true")
    error.set_defaults(func=cmd_record_error)

    card = sub.add_parser("add-card")
    card.add_argument("--course", required=True)
    card.add_argument("--point", required=True)
    card.add_argument("--front", required=True)
    card.add_argument("--back", required=True)
    card.add_argument("--due", default=dt.date.today().isoformat())
    card.add_argument("--priority", choices=["low", "normal", "high"], default="normal")
    card.set_defaults(func=cmd_add_card)

    status = sub.add_parser("status")
    status.add_argument("--course", required=True)
    status.set_defaults(func=cmd_status)

    summary = sub.add_parser("summary")
    summary.add_argument("--course", required=True)
    summary.set_defaults(func=cmd_summary)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
