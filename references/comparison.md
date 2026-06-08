# Comparison Notes

Research date: 2026-06-07.

## Related Staged Exam-Prep Skill

Observed structure:

- `SKILL.md` orchestrates the workflow.
- `stages/` contains four prompt files.
- `configs/example.yaml` defines a course profile.
- A local course directory stores user configs and progress.
- `.trae/rules/project_rules.md` adds Trae trigger support.

Strengths:

- Clear four-stage teaching loop.
- Good use of cognitive load, generation, retrieval practice, and remediation.
- Terminal-first and easy to install.
- Strong fit for qualitative university exams.

Gaps to improve:

- Progress is Markdown-first, difficult to query reliably.
- Source grounding is not mandatory, so hallucinated exam predictions can look authoritative.
- Quantitative, programming, language, and formula-heavy courses are mostly out of scope.
- Random drill selection is not reproducible.
- Long stage prompts can be loaded even when a compact session would suffice.
- Review scheduling is coarse; stubborn points are deferred but not systematically queued.
- Cross-agent support is partial.

## Related Projects and Practices

Human Skill Tree shows broader learning-science coverage: active recall, spaced repetition, interleaving, Socratic tutoring, and domain-specific tutor personas.

skill-cli emphasizes progressive disclosure and claims large token savings by loading quick references first and details only when needed.

OpenClaw and OpenCode docs confirm the shared `SKILL.md` folder model, but platform install paths and metadata expectations differ.

## Design Response

Pass All Exams keeps the useful staged-study baseline, then adds:

- compact default loop
- evidence sections
- JSON/JSONL state
- review cards
- broader subject adapters
- cross-platform install script
- validation script
