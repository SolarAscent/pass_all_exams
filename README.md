<p align="right">
  <strong>EN</strong> | <a href="./README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <img src="docs/hero.svg" alt="Pass All Exams" width="760"/>
</p>

<h1 align="center">Pass all exams</h1>

<p align="center">
  <em>Finals week and still not ready? Don't panic. This is the AI era: use a skill to make every review session count twice.</em>
</p>

<p align="center">
  <strong>Evidence-grounded exam prep for Codex, Claude Code, OpenClaw, and OpenCode.</strong>
</p>

<p align="center">
  Turn teacher notes, syllabi, past papers, and rough knowledge lists into a compact loop:
  map what can be tested, learn one point, retrieve it, repair mistakes, and schedule review.
</p>

<p align="center">
  <a href="https://github.com/SolarAscent/pass_all_exams/releases/tag/v2.0.0"><img src="https://img.shields.io/github/v/release/SolarAscent/pass_all_exams?style=flat-square&label=release&labelColor=111827&color=2563EB" alt="Latest release"/></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-16A34A?style=flat-square&labelColor=111827" alt="MIT license"/></a>
  <img src="https://img.shields.io/badge/Codex-supported-2563EB?style=flat-square&labelColor=111827" alt="Codex supported"/>
  <img src="https://img.shields.io/badge/Claude%20Code-supported-D97706?style=flat-square&labelColor=111827" alt="Claude Code supported"/>
  <img src="https://img.shields.io/badge/OpenClaw-supported-0F766E?style=flat-square&labelColor=111827" alt="OpenClaw supported"/>
  <img src="https://img.shields.io/badge/OpenCode-supported-9333EA?style=flat-square&labelColor=111827" alt="OpenCode supported"/>
  <img src="https://img.shields.io/badge/token%20mode-compact-F59E0B?style=flat-square&labelColor=111827" alt="Compact token mode"/>
</p>

<br/>

## What It Does

Pass All Exams is an Agent Skill for students who need a practical review system, not another long pile of notes.

Its architecture is built around seven small pieces: file ingestion, intake, mapping, teaching, drilling, repairing, and review scheduling. Microsoft [MarkItDown](https://github.com/microsoft/markitdown) converts uploaded PDFs, Word documents, PowerPoint decks, spreadsheets, images, audio, HTML, CSV/JSON/XML, ZIP files, EPubs, and other supported formats into Markdown before the study loop starts. `SKILL.md` stays light so the agent can load quickly; detailed stage rules live in `references/`; deterministic local state is handled by `scripts/examctl.py`; material ingestion is handled by `scripts/ingest_materials.py`; install and packaging helpers keep the same workflow portable across supported agents.

The default session is deliberately small:

```text
one course -> one high-yield point -> one explanation -> one retrieval question -> one repair or review card
```

## New to Agent Skills?

Pass All Exams runs inside agent tools that can load a `SKILL.md` folder and follow reusable workflows. You do not need to understand their internals, but you do need one compatible agent installed.

| Tool | What it is | Official link |
|---|---|---|
| Codex | OpenAI's coding agent, available through ChatGPT and local developer workflows. | [openai.com/codex](https://openai.com/codex/) |
| Claude Code | Anthropic's agentic coding assistant. Personal skills live in `~/.claude/skills`; project skills live in `.claude/skills`. | [Claude Code docs](https://code.claude.com/docs/en/overview) |
| OpenClaw | An open agent platform with a skill system built around `SKILL.md`. | [docs.openclaw.ai](https://docs.openclaw.ai/) |
| OpenCode | A terminal coding agent that discovers project and global Agent Skills. | [opencode.ai/docs](https://opencode.ai/docs/) |

## Why It Is Different

| Problem in ordinary AI review | Pass All Exams response |
|---|---|
| The model writes long notes but never checks recall. | Every taught point is followed by a retrieval step. |
| Exam predictions can sound teacher-confirmed when they are not. | Answers separate `Source-backed`, `Reasonable inference`, and `Needs confirmation`. |
| Chat history becomes expensive to reread. | Progress lives in `state.json`, `errors.jsonl`, and `cards.jsonl`. |
| Cram tools often fit only humanities courses. | The pipeline includes qualitative, quantitative, programming, language, and memorization-heavy patterns. |
| Mistakes get re-explained in the same words. | Errors are classified, repaired with a new representation, then retested from a new angle. |

## Install

The repository name is `pass_all_exams`; the skill name inside the agent is `pass-all-exams`.

### Option 0: One-Click Install (Recommended)

This single command clones the project, installs MarkItDown for file conversion, and copies the skill into your agent's directory:

```bash
curl -fsSL https://raw.githubusercontent.com/SolarAscent/pass_all_exams/main/scripts/quick-install.sh | bash -s -- <agent>
```

Replace `<agent>` with your agent key:

| Agent | Command |
|---|---|
| Claude Code, global | `curl -fsSL https://raw.githubusercontent.com/SolarAscent/pass_all_exams/main/scripts/quick-install.sh \| bash -s -- claude` |
| Claude Code, current project only | `curl -fsSL https://raw.githubusercontent.com/SolarAscent/pass_all_exams/main/scripts/quick-install.sh \| bash -s -- claude-project` |
| Codex | `curl -fsSL https://raw.githubusercontent.com/SolarAscent/pass_all_exams/main/scripts/quick-install.sh \| bash -s -- codex` |
| OpenClaw | `curl -fsSL https://raw.githubusercontent.com/SolarAscent/pass_all_exams/main/scripts/quick-install.sh \| bash -s -- openclaw` |
| OpenCode, global | `curl -fsSL https://raw.githubusercontent.com/SolarAscent/pass_all_exams/main/scripts/quick-install.sh \| bash -s -- opencode` |
| OpenCode, current project only | `curl -fsSL https://raw.githubusercontent.com/SolarAscent/pass_all_exams/main/scripts/quick-install.sh \| bash -s -- opencode-project` |

Add `--skip-deps` before the agent name if you prefer to install Python dependencies manually later.

### Option 1: Install from Git

```bash
git clone https://github.com/SolarAscent/pass_all_exams.git
cd pass_all_exams
```

Install the file-conversion dependency if you want to use uploaded files:

```bash
python3 -m pip install -r requirements-markitdown.txt
```

Then install for your agent:

| Agent | Command |
|---|---|
| Codex | `bash scripts/install.sh codex` |
| Claude Code, global | `bash scripts/install.sh claude` |
| Claude Code, current project only | `bash scripts/install.sh claude-project` |
| OpenClaw | `bash scripts/install.sh openclaw` |
| OpenCode, global | `bash scripts/install.sh opencode` |
| OpenCode, current project only | `bash scripts/install.sh opencode-project` |

### Option 2: Manual Paths

If you prefer to clone directly into the skill directory:

```bash
# Codex
git clone https://github.com/SolarAscent/pass_all_exams.git ~/.codex/skills/pass-all-exams

# Codex with CODEX_HOME
git clone https://github.com/SolarAscent/pass_all_exams.git "$CODEX_HOME/skills/pass-all-exams"

# Claude Code global
git clone https://github.com/SolarAscent/pass_all_exams.git ~/.claude/skills/pass-all-exams

# Claude Code project-local
git clone https://github.com/SolarAscent/pass_all_exams.git .claude/skills/pass-all-exams

# OpenClaw
git clone https://github.com/SolarAscent/pass_all_exams.git ~/.openclaw/skills/pass-all-exams

# OpenCode global
git clone https://github.com/SolarAscent/pass_all_exams.git ~/.config/opencode/skill/pass-all-exams

# OpenCode project-local
git clone https://github.com/SolarAscent/pass_all_exams.git .opencode/skill/pass-all-exams
```

### Option 3: Download `.skill`

Download the release asset:

```text
https://github.com/SolarAscent/pass_all_exams/releases/download/v2.0.0/pass-all-exams.skill
```

Use this when your agent or UI supports uploading skill archives.

## Quick Start

After installation, start with a natural request:

```text
/exam Organizational Behavior start
```

or:

```text
Use pass-all-exams to help me review Organizational Behavior.
The exam has multiple choice, short answer, and case analysis.
My must-know topics are Hawthorne studies and expectancy theory.
```

For Chinese courses:

```text
/exam 组织行为学 start
```

or:

```text
帮我用 pass-all-exams 复习组织行为学。考试题型是选择题、简答题和案例分析。
老师强调必考：霍桑实验、期望理论。我会继续粘贴课堂笔记。
```

If you have files, ingest them first:

```bash
python3 scripts/ingest_materials.py \
  --course "Organizational Behavior" \
  ~/Downloads/syllabus.pdf \
  ~/Downloads/week-1-slides.pptx \
  ~/Downloads/review-notes.docx
```

Converted Markdown is saved under the course's local `materials/` directory and reused by later stages.

## The Review Loop

```text
Intake
  collect course, exam date, question types, materials, must-know points

Ingest
  convert uploaded files to Markdown with Microsoft MarkItDown and cache by SHA-256

Map
  split materials into exam-sized points and mark source confidence

Teach
  explain one point with concrete-first, <=3 chunks, one self-generation prompt

Drill
  test by real exam type: choice, case, calculation, code tracing, short answer...

Repair
  classify the miss, switch method, retest with a new angle

Review
  create same-day, next-day, 3-day, and final-day retrieval cards
```

## Evidence Contract

Every substantive explanation or grading response should make the source status visible:

```text
Source-backed:
- Directly supported by the notes, syllabus, teacher wording, or pasted material.

Reasonable inference:
- Useful exam-prep inference from standard course knowledge.

Needs confirmation:
- Things that may depend on your teacher, textbook edition, or local exam scope.
```

This is the main hallucination-control layer. If you provide no materials, the skill will operate in general-knowledge mode and should not pretend to know your teacher's real exam scope.

## Commands

| Command | Use |
|---|---|
| `/exam <course> start` | Create or refresh a course plan. |
| `/cram <course> start` | Alias for students coming from cram-style workflows. |
| `/exam <course> resume` | Continue from saved progress. |
| `/exam <course> drill` | Generate practice from weak points and due review cards. |
| `/exam <course> retry <point>` | Reteach, retest, and update one weak point. |
| `/exam <course> summary` | Produce a final-day checklist. |

## Local State

Course state is stored locally:

```text
~/.pass-all-exams/courses/<course-slug>/
```

Inside each course:

| File | Purpose |
|---|---|
| `course.yaml` | Course profile: exam types, materials, must-know points, preferences. |
| `state.json` | Current stage and point-level status. |
| `materials/` | MarkItDown-converted Markdown files. |
| `materials.jsonl` | Material index: source path, SHA-256, output path, title, byte count, status. |
| `errors.jsonl` | Wrong answers and diagnosis history. |
| `cards.jsonl` | Retrieval cards and due dates. |
| `sessions.jsonl` | Optional session log. |

Useful helper commands:

```bash
python3 scripts/examctl.py init --course "Organizational Behavior"
python3 scripts/examctl.py status --course "Organizational Behavior"
python3 scripts/examctl.py summary --course "Organizational Behavior"
```

Convert uploaded or downloaded course files:

```bash
python3 scripts/ingest_materials.py --course "Organizational Behavior" ~/Downloads/syllabus.pdf
```

By default, ingestion accepts local files only. Trusted URLs require `--allow-url` because MarkItDown reads with the privileges of the current process.

Audio transcription may require system audio tooling such as `ffmpeg`; ordinary PDF/Office/text conversion does not.

Example records:

```bash
python3 scripts/examctl.py record-point \
  --course "Organizational Behavior" \
  --point "Expectancy theory" \
  --level must \
  --status taught \
  --source material

python3 scripts/examctl.py record-error \
  --course "Organizational Behavior" \
  --point "Expectancy theory" \
  --reason confusion \
  --question-type "multiple choice" \
  --must-know
```

## Token Modes

| Mode | Best for | Behavior |
|---|---|---|
| `compact` | Most cram sessions | One point, one example, one question, one correction. |
| `standard` | Normal weekly review | Adds one extra example and a relation to a prior point. |
| `deep` | Hard subjects or high-stakes finals | Adds derivation, edge cases, and mixed practice. |

The default is `compact`. The skill also uses progressive disclosure: `SKILL.md` stays short, while stage rules live in `references/` and are loaded only when needed.

## Supported Course Types

| Course type | Examples | Special handling |
|---|---|---|
| Humanities and social science | law, politics, sociology, education | definitions, comparisons, case-analysis score skeletons |
| Business and management | organizational behavior, marketing, accounting theory | frameworks, traps, case application |
| Quantitative courses | calculus, statistics, economics methods | formula conditions, worked examples, calculation error diagnosis |
| Programming courses | data structures, databases, OS, Python/C/Java | trace questions, bug repair, complexity explanation |
| Language and memorization-heavy courses | English, history, medicine basics | cloze, recall cards, contrast tables |

## Build a Skill Package

Create an uploadable `.skill` archive:

```bash
python3 scripts/package_skill.py
```

Validate the package layout:

```bash
python3 scripts/validate_skill.py
python3 -m py_compile scripts/examctl.py scripts/ingest_materials.py scripts/validate_skill.py scripts/package_skill.py
```

## Repository Layout

```text
pass_all_exams/
├── CHANGELOG.md
├── PROJECT_CHECK.md
├── SKILL.md                    # agent-facing entry point
├── agents/openai.yaml          # Codex UI metadata
├── configs/example.yaml        # sample course profile
├── requirements-markitdown.txt # Microsoft MarkItDown dependency set
├── references/
│   ├── pipeline.md             # detailed review workflow
│   ├── prompt-patterns.md      # reusable prompt shapes
│   ├── platforms.md            # Codex/Claude Code/OpenClaw/OpenCode notes
│   └── comparison.md           # design notes from related projects
├── scripts/
│   ├── examctl.py              # deterministic course state helper
│   ├── ingest_materials.py     # MarkItDown material ingestion helper
│   ├── install.sh              # cross-agent install helper
│   ├── package_skill.py        # .skill archive builder
│   └── validate_skill.py       # portable package validator
└── docs/hero.svg
```

## Privacy

All course state is local by default. The skill does not require an external service, database, or account. Your notes, wrong answers, and review cards remain in `~/.pass-all-exams/` unless you explicitly move or share them.

## Acknowledgments

This project uses [Microsoft MarkItDown](https://github.com/microsoft/markitdown) to convert uploaded course materials (PDF, Word, PowerPoint, Excel, images, audio, HTML, CSV, JSON, XML, ZIP, EPub, and more) into Markdown for the study pipeline. MarkItDown is developed and maintained by Microsoft.

## License

[MIT](LICENSE)
