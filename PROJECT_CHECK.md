# Project Check

## 2.0.0 - 2026-06-08

Environment used for MarkItDown validation:

- Python: 3.12.13
- MarkItDown: 0.1.6, installed through `requirements-markitdown.txt`
- Temporary venv: `/tmp/pass-all-exams-v2-venv`

Checks completed:

- `python3 scripts/validate_skill.py` passed.
- `python3 -m py_compile scripts/examctl.py scripts/ingest_materials.py scripts/validate_skill.py scripts/package_skill.py` passed.
- `git diff --check` passed.
- `python3 -m pip install -r requirements-markitdown.txt` passed in a clean temporary virtual environment.
- `scripts/ingest_materials.py` converted a local Markdown course file into `materials/<name>-<sha>.md`.
- `materials.jsonl` recorded source path, SHA-256 hash, output path, title, byte count, and conversion status.
- `state.json` updated `counts.materials`.
- Re-ingesting the same unchanged file returned `status: cached`.
- URL ingestion was rejected by default and required explicit `--allow-url`.
- `.skill` package was rebuilt with the v2.0.0 files.

Known operational note:

- Audio transcription can require system audio tooling such as `ffmpeg`. This does not affect ordinary PDF, Office, HTML, CSV/JSON/XML, or text conversion.
