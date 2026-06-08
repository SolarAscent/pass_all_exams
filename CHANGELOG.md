# Changelog

## 2.0.0 - 2026-06-08

- Added Microsoft MarkItDown-powered material ingestion for uploaded course files.
- Added `scripts/ingest_materials.py` to convert PDFs, Word documents, PowerPoint decks, spreadsheets, images, audio, HTML, CSV/JSON/XML, ZIP files, EPubs, and other MarkItDown-supported inputs into Markdown.
- Added local material storage under `~/.pass-all-exams/courses/<course-slug>/materials/`.
- Added `materials.jsonl` indexing with source path, SHA-256 hash, converted output path, title, byte count, and conversion status.
- Added hash-based caching so unchanged files are not converted repeatedly.
- Added `requirements-markitdown.txt` for installing the optional file-conversion dependency set.
- Updated README, Chinese README, SKILL instructions, and platform references for the file-upload workflow.

## 0.1.0 - 2026-06-07

- Initial portable Agent Skill for Codex, Claude Code, OpenClaw, and OpenCode.
- Added evidence-grounded exam-prep loop, local JSON/JSONL progress, review cards, install helper, package builder, and release archive.
