# Platform Notes

Pass All Exams is a plain Agent Skill folder with `SKILL.md` at the root.

## Codex

Install globally:

```bash
git clone https://github.com/SolarAscent/pass_all_exams.git ~/.codex/skills/pass-all-exams
```

If `CODEX_HOME` is set:

```bash
git clone https://github.com/SolarAscent/pass_all_exams.git "$CODEX_HOME/skills/pass-all-exams"
```

Codex also reads `agents/openai.yaml` for UI metadata.

## OpenClaw

OpenClaw/ClawHub accepts a folder with `SKILL.md` or `skill.md`. Frontmatter `description` is used for search, and runtime needs can be declared under `metadata.openclaw`.

Manual global install:

```bash
git clone https://github.com/SolarAscent/pass_all_exams.git ~/.openclaw/skills/pass-all-exams
```

## OpenCode

OpenCode discovers:

- project: `.opencode/skill/<name>/SKILL.md`
- global: `~/.config/opencode/skill/<name>/SKILL.md`
- Claude-compatible project/global paths

Install globally:

```bash
git clone https://github.com/SolarAscent/pass_all_exams.git ~/.config/opencode/skill/pass-all-exams
```

Install project-local:

```bash
git clone https://github.com/SolarAscent/pass_all_exams.git .opencode/skill/pass-all-exams
```

## Installer Script

From the repository root:

```bash
bash scripts/install.sh codex
bash scripts/install.sh openclaw
bash scripts/install.sh opencode
```

The script copies the current folder to the target skill directory and excludes `.git` and local course state.
