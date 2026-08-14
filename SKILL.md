---
name: pass-all-exams
description: Use this skill for Chinese or bilingual exam prep, final review, file-based course material ingestion, uploaded PDFs/Word/PPT/Excel conversion, cram sessions, course revision, mock tests, wrong-answer remediation, spaced review, or commands like /exam, /cram, pass all exams. It helps students turn course materials, syllabi, teacher重点, past papers, and exam types into a low-token, evidence-grounded study loop for Codex, Claude Code, OpenClaw, and OpenCode.
version: 3.0.0
license: MIT
compatibility: codex, claude-code, openclaw, opencode
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🎓"
    homepage: "https://github.com/SolarAscent/pass_all_exams"
---

# Pass All Exams

Exam-prep skill for short, high-yield study sessions. It combines MarkItDown material ingestion, evidence labels, machine-readable progress, spaced review, and cross-agent installation.

## Commands

- `/exam <course> start` or `/cram <course> start`: create or refresh a course plan.
- `/exam <course> resume`: continue from the next pending item.
- `/exam <course> drill`: generate retrieval practice from current weak points.
- `/exam <course> retry <point>`: reteach, retest, and log one weak point.
- `/exam <course> summary`: produce final-day checklist.

## First Move

If the course is new, collect only the missing fields:

1. Course name and exam date, if known.
2. Exam type: closed-book/open-book, question formats, scoring hints.
3. Materials: pasted notes, uploaded file paths, syllabus, teacher重点, past papers.
4. Knowledge points, marking must-know items separately.
5. Target mode: `compact`, `standard`, or `deep`.

Create local state with:

```bash
python3 scripts/examctl.py init --course "<course>"
```

When the user provides local files, convert them before mapping:

```bash
python3 scripts/ingest_materials.py --course "<course>" "<file1>" "<file2>"
```

Use `~/.pass-all-exams/courses/<slug>/` for state. Never overwrite a student's notes or progress without asking.

Converted materials are stored under `~/.pass-all-exams/courses/<slug>/materials/` and indexed in `materials.jsonl`. Read those Markdown files for the Map stage instead of reparsing the original uploads.

## Core Loop

Run one narrow stage at a time:

1. **Map**: split converted Markdown materials into exam-sized points and mark source confidence.
2. **Teach**: explain one point with concrete-first, <=3 chunks, and one self-generation prompt.
3. **Drill**: test by actual exam type. Mix active recall, interleaving, and traps.
4. **Diagnose**: classify errors as confusion, missing term, logic reversal, or transfer failure.
5. **Repair**: switch method, retest with a new angle, then mark corrected or stubborn.
6. **Review**: schedule tomorrow/3-day/final-day retrieval for stubborn or high-value points.

For detailed stage rules, load `references/pipeline.md` only when implementing a session.

## Anti-Hallucination Contract

Every substantive teaching or answer-checking response must separate:

- `资料依据`: what is directly supported by user materials.
- `合理推断`: useful inference from standard course knowledge.
- `待确认`: facts that need the student's teacher, textbook, or notes.

If no materials are provided, say that the session is operating in general-knowledge mode and ask for at least a syllabus or point list before producing high-stakes predictions.

## Token Budget Rules

- Default to `compact`: one point, one example, one question, one correction.
- Do not load all references. Load only the file needed for the current action.
- Prefer tables and JSONL state over long prose history.
- Summarize prior work from `state.json`, `cards.jsonl`, and `errors.jsonl` instead of rereading chat.

Use `references/prompt-patterns.md` for reusable prompt shapes and `references/platforms.md` for installation paths.
