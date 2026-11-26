#!/usr/bin/env bash
# Install the hyperframes skills into a Claude config dir
# (a project's .claude/ or ~/.claude/), laid out as its own installer does.
# Usage: install_skills.sh <dir holding a hyperframes/ checkout> <target .claude dir>
set -euo pipefail
SRC=$1
DEST=$2
HF=$SRC/hyperframes
SK=$DEST/skills
mkdir -p "$SK"

# --- hyperframes: every published skill, as siblings ---
for d in "$HF"/skills/*/; do
  name=$(basename "$d")
  [ -f "$d/SKILL.md" ] || continue
  rm -rf "${SK:?}/$name"
  cp -a "$d" "$SK/$name"
done
cp -p "$HF/LICENSE" "$SK/hyperframes/LICENSE"

find "$SK" -name __pycache__ -type d -prune -exec rm -rf {} +
echo "installed into $DEST"
