#!/usr/bin/env bash
set -euo pipefail

agent="${1:-codex}"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case "$agent" in
  codex)
    base="${CODEX_HOME:-$HOME/.codex}/skills"
    ;;
  openclaw)
    base="$HOME/.openclaw/skills"
    ;;
  opencode)
    base="$HOME/.config/opencode/skill"
    ;;
  opencode-project)
    base="$PWD/.opencode/skill"
    ;;
  *)
    echo "usage: bash scripts/install.sh [codex|openclaw|opencode|opencode-project]" >&2
    exit 2
    ;;
esac

target="$base/pass-all-exams"
mkdir -p "$base"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete --exclude ".git" --exclude ".pass-all-exams" "$repo_root/" "$target/"
else
  rm -rf "$target"
  mkdir -p "$target"
  cp -R "$repo_root/." "$target/"
  rm -rf "$target/.git" "$target/.pass-all-exams"
fi

echo "installed pass-all-exams to $target"
