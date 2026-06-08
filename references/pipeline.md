# Pass All Exams Pipeline

This reference is loaded when running a real study session or editing the skill.

## Architecture Notes

The skill is organized around a staged exam-prep loop:

- staged flow instead of one giant prompt
- cognitive load control through one-point sessions
- concrete-first teaching
- generation before answer reveal
- retrieval practice and remediation
- progress persistence through local state

Additional design choices:

- evidence labels reduce hallucination and make weak sourcing visible
- machine-readable `state.json`, `cards.jsonl`, and `errors.jsonl`
- MarkItDown ingestion normalizes uploaded course files into Markdown before mapping
- token modes: compact, standard, deep
- supports qualitative, quantitative, code, language, and memorization-heavy courses
- spaced review queue instead of only "try tomorrow"
- deterministic scripts for state and summaries
- cross-agent install guidance for Codex, OpenClaw, and OpenCode

## Stage 0: Intake

Collect missing information in the smallest number of questions. Prefer one bundled question when the user already supplied context.

Required:

- course
- exam date or time budget, if known
- exam types
- knowledge points or source materials
- must-know points, if any

Optional:

- textbook/version
- teacher wording
- past papers
- grading rubrics
- student's self-rated weak areas

Create state:

```bash
python3 scripts/examctl.py init --course "<course>"
```

If the user provides files, convert them before Stage 1:

```bash
python3 scripts/ingest_materials.py --course "<course>" "<path/to/file.pdf>" "<path/to/slides.pptx>"
```

Use converted Markdown under `~/.pass-all-exams/courses/<slug>/materials/` as the source for mapping. The ingestion index is `materials.jsonl`.

MarkItDown requires:

```bash
python3 -m pip install -r requirements-markitdown.txt
```

Prefer local files. Only use `--allow-url` for trusted URLs because MarkItDown performs I/O with the privileges of the current process.

Audio transcription may require system audio tooling such as `ffmpeg`; do not treat an audio warning as a failure for ordinary PDF, Office, or text files.

## Stage 1: Map

Turn materials into exam-sized points.

Output:

```text
## Knowledge Map
1. <point> [must|key|support] [source: material|inferred|needs-confirmation]
   - boundaries:
   - likely question types:
   - prerequisites:
   - common traps:
```

Rules:

- A point should be teachable in 3-7 minutes.
- Preserve teacher wording when supplied.
- For quantitative courses, separate concept, formula conditions, derivation intuition, and problem pattern.
- For programming courses, separate concept, API/syntax, tracing, and debugging pattern.
- Mark unsupported predictions as `needs-confirmation`.

## Stage 2: Teach

Teach one point at a time.

Compact mode:

1. concrete scene or minimal worked example
2. <=3 chunks
3. one contrast/trap
4. one self-generation question

Standard mode adds one more example and one relation to a prior point.

Deep mode adds derivation, edge cases, and a mini mixed drill.

Always end with a student action:

- "用一句话复述"
- "把公式条件列出来"
- "先判断用哪个理论"
- "先写伪代码"

## Stage 3: Drill

Use exam types, not generic quizzes.

Question families:

- objective: choice, judgment, fill blank
- short answer: term explanation, compare, list, mechanism
- application: scenario, case, policy, legal analysis
- quantitative: formula choice, calculation, proof sketch, error analysis
- programming: trace output, fix bug, explain complexity, implement small function
- language: translation, cloze, writing outline, grammar correction

Coverage:

- must: every declared exam type
- key: 1-2 likely types
- support: only if prerequisite or repeated mistake

Record misses:

```bash
python3 scripts/examctl.py record-error --course "<course>" --point "<point>" --reason "<reason>"
```

## Stage 4: Diagnose and Repair

Classify root cause:

- `confusion`: mixed with another point
- `missing-term`: forgot keyword, condition, or step
- `logic-reversal`: causal direction or exception is wrong
- `transfer-failure`: can recite but cannot apply
- `calculation`: arithmetic/algebra/procedure error
- `expression`: knows idea but cannot write scoreable answer

Repair mapping:

- confusion -> contrast table and discriminating question
- missing-term -> mnemonic plus blank recall
- logic-reversal -> counterexample
- transfer-failure -> new scenario, same principle
- calculation -> slow worked example, then one near-transfer problem
- expression -> scoring skeleton and rewrite

Do not repeat the same explanation. Change representation.

## Stage 5: Review

Schedule review cards:

- same day: all misses
- next day: stubborn and must
- 3 days: corrected must/key
- final day: must, traps, formula conditions, score skeletons

Use `cards.jsonl` as append-only retrieval cards. A card should be short enough to answer from memory.

## Final-Day Summary

Include:

- must-know status
- stubborn points
- top traps
- formulas or frameworks
- "do not spend more time on" list
- 30/60/120 minute plan
