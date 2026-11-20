#!/usr/bin/env bash
# Installs the merged ponytail skill for ALL Claude Code sessions on this machine
# and makes it the default for every coding task. Safe to re-run.
set -euo pipefail
src="$(cd "$(dirname "$0")/.." && pwd)/.claude/skills/ponytail"
dst="$HOME/.claude/skills/ponytail"
mkdir -p "$dst" "$HOME/.claude"
cp "$src/SKILL.md" "$dst/SKILL.md"
md="$HOME/.claude/CLAUDE.md"
grep -q 'ponytail skill' "$md" 2>/dev/null || cat >> "$md" <<'TXT'

# Default coding style
On every coding task, use the ponytail skill (lazy senior dev mode: smallest complete change, report skipped work and risks) unless I say "normal mode".
TXT
echo "Installed: $dst/SKILL.md (+ default rule in $md)"
