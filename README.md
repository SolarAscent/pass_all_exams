# Pass All Exams

Evidence-grounded exam-prep skill for Codex, OpenClaw, and OpenCode.

It keeps the useful cram-engine idea: map knowledge, teach one point, drill by exam type, remediate mistakes. It adds source labels, JSON/JSONL progress, spaced review cards, quantitative/programming adapters, and compact prompts to reduce token use.

## Install

```bash
git clone https://github.com/SolarAscent/pass_all_exams.git
cd pass_all_exams
bash scripts/install.sh codex
```

Other agents:

```bash
bash scripts/install.sh openclaw
bash scripts/install.sh opencode
```

OpenCode project-local:

```bash
bash scripts/install.sh opencode-project
```

## Use

Say:

```text
/exam 组织行为学 start
```

or:

```text
帮我用 pass-all-exams 复习这门课，考试题型是选择题、简答和案例分析。
```

## State

Course state lives under:

```text
~/.pass-all-exams/courses/<course-slug>/
```

Useful commands:

```bash
python3 scripts/examctl.py init --course "组织行为学"
python3 scripts/examctl.py status --course "组织行为学"
python3 scripts/examctl.py summary --course "组织行为学"
```

## Why This Exists

Raw AI chat often turns review into long notes. This skill keeps the agent in a loop that students actually need before exams:

1. Identify what can be tested.
2. Explain only the next high-yield point.
3. Force recall.
4. Diagnose the miss.
5. Retest from a different angle.
6. Schedule the next review.

## License

MIT
