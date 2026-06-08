#!/usr/bin/env bash
# quick-install.sh — One-click installer for pass-all-exams Agent Skill.
#
# Usage (recommended):
#   curl -fsSL https://raw.githubusercontent.com/SolarAscent/pass_all_exams/main/scripts/quick-install.sh | bash -s -- <agent>
#
# Supported agents: codex | claude | claude-project | openclaw | opencode | opencode-project
#
# What this script does:
#   1. Clones the pass_all_exams repo to a temporary directory.
#   2. Installs markitdown[all] via pip (skip with --skip-deps).
#   3. Copies the skill into your agent's skill directory.
#   4. Cleans up the temporary clone.
#   5. Prints a success message with next steps.
#
# Flags (place before the agent name):
#   --skip-deps    Skip pip install of markitdown[all].

set -euo pipefail

SKIP_DEPS=false
AGENT=""

for arg in "$@"; do
  case "$arg" in
    --skip-deps) SKIP_DEPS=true ;;
    *) AGENT="$arg" ;;
  esac
done

if [ -z "$AGENT" ]; then
  echo "usage: bash quick-install.sh [--skip-deps] <agent>" >&2
  echo "  agents: codex | claude | claude-project | openclaw | opencode | opencode-project" >&2
  exit 2
fi

case "$AGENT" in
  codex)         BASE="${CODEX_HOME:-$HOME/.codex}/skills" ;;
  claude|claude-code|claudecode) BASE="$HOME/.claude/skills" ;;
  claude-project|claude-code-project|claudecode-project) BASE="$PWD/.claude/skills" ;;
  openclaw)      BASE="$HOME/.openclaw/skills" ;;
  opencode)      BASE="$HOME/.config/opencode/skill" ;;
  opencode-project) BASE="$PWD/.opencode/skill" ;;
  *)
    echo "error: unknown agent '$AGENT'" >&2
    echo "  agents: codex | claude | claude-project | openclaw | opencode | opencode-project" >&2
    exit 2
    ;;
esac

REPO="https://github.com/SolarAscent/pass_all_exams.git"
TMPDIR=$(mktemp -d /tmp/pass-all-exams-XXXXXXX)
TARGET="$BASE/pass-all-exams"

cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

echo "→ Cloning pass_all_exams to temporary directory..."
git clone --quiet --depth 1 "$REPO" "$TMPDIR"

if [ "$SKIP_DEPS" = false ]; then
  echo "→ Installing markitdown[all] (file conversion support)..."
  if command -v python3 >/dev/null 2>&1; then
    python3 -m pip install --quiet -r "$TMPDIR/requirements-markitdown.txt" 2>&1 | tail -1 || {
      echo "! pip install failed. You can install dependencies later with:"
      echo "  python3 -m pip install -r requirements-markitdown.txt"
      echo "  (see https://github.com/SolarAscent/pass_all_exams for details)"
    }
  else
    echo "! python3 not found. Skipping dependency install."
    echo "  Install python3 and run: python3 -m pip install 'markitdown[all]'"
  fi
fi

echo "→ Installing pass-all-exams to $TARGET ..."
mkdir -p "$BASE"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete --exclude ".git" --exclude ".pass-all-exams" "$TMPDIR/" "$TARGET/"
else
  rm -rf "$TARGET"
  mkdir -p "$TARGET"
  cp -R "$TMPDIR/." "$TARGET/"
  rm -rf "$TARGET/.git" "$TARGET/.pass-all-exams"
fi

echo ""
echo "✅ pass-all-exams installed to $TARGET"
echo ""
echo "Quick start:"
echo "  /exam <course> start"
echo ""
echo "To convert course files first:"
echo "  python3 $TARGET/scripts/ingest_materials.py --course \"<course>\" <file1> <file2>"
echo ""
echo "See https://github.com/SolarAscent/pass_all_exams for full docs."
