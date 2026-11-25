#!/usr/bin/env bash
# Install the claude-ads and hyperframes skills into a Claude config dir
# (a project's .claude/ or ~/.claude/), laid out as their own installers do.
# Usage: install_skills.sh <dir holding claude-ads/ and hyperframes/ checkouts> <target .claude dir>
set -euo pipefail
SRC=$1
DEST=$2
ADS=$SRC/claude-ads
HF=$SRC/hyperframes
SK=$DEST/skills
AG=$DEST/agents
mkdir -p "$SK" "$AG"

copy_glob() { # copy_glob <dst dir> <files...>
  local dst=$1; shift
  mkdir -p "$dst"
  for f in "$@"; do [ -f "$f" ] && [ ! -L "$f" ] && cp -p "$f" "$dst/"; done
  return 0
}

# --- claude-ads: conductor skill "ads" (same file set as its install.sh) ---
rm -rf "$SK/ads"
copy_glob "$SK/ads" "$ADS/ads/SKILL.md" "$ADS/requirements.txt" "$ADS/requirements.lock" "$ADS/LICENSE"
copy_glob "$SK/ads/references" "$ADS"/ads/references/*.md
copy_glob "$SK/ads/agents" "$ADS"/ads/agents/*.yaml "$ADS"/agents/*.md
copy_glob "$SK/ads/scripts" "$ADS"/scripts/*.py
copy_glob "$SK/ads/scripts/claude_ads_core" "$ADS"/claude_ads_core/*.py
copy_glob "$SK/ads/scripts/claude_ads_core/adapters" "$ADS"/claude_ads_core/adapters/*.py
copy_glob "$SK/ads/scripts/claude_ads_core/schemas/v1" "$ADS"/claude_ads_core/schemas/v1/*.json
grep -vE '^\s*(#|$)' "$ADS/control-plane/runtime-resources.txt" | while read -r rel; do
  case "$rel" in control-plane/*) ;; *) echo "skip $rel" >&2; continue ;; esac
  case "$rel" in *..*) echo "skip $rel" >&2; continue ;; esac
  mkdir -p "$SK/ads/$(dirname "$rel")"
  cp -p "$ADS/$rel" "$SK/ads/$rel"
done
# --- claude-ads: workflow and platform skills, as siblings of ads/ ---
for d in "$ADS"/skills/*/; do
  name=$(basename "$d")
  [ -f "$d/SKILL.md" ] || continue
  rm -rf "${SK:?}/$name"
  copy_glob "$SK/$name" "$d/SKILL.md"
  [ -d "$d/assets" ] && copy_glob "$SK/$name/assets" "$d"/assets/*.md
done
# --- claude-ads: subagents (its installer puts these in the agents dir) ---
copy_glob "$AG" "$ADS"/agents/*.md

# --- hyperframes: every published skill, as siblings ---
for d in "$HF"/skills/*/; do
  name=$(basename "$d")
  [ -f "$d/SKILL.md" ] || continue
  rm -rf "${SK:?}/$name"
  cp -a "$d" "$SK/$name"
done
cp -p "$HF/LICENSE" "$SK/hyperframes/LICENSE"

# --- vercel-labs/skills: find-skills (optional: only if that checkout is given) ---
VS=$SRC/vercel-skills
if [ -f "$VS/skills/find-skills/SKILL.md" ]; then
  rm -rf "$SK/find-skills"
  copy_glob "$SK/find-skills" "$VS/skills/find-skills/SKILL.md" "$VS/LICENSE"
fi

find "$SK" -name __pycache__ -type d -prune -exec rm -rf {} +
echo "installed into $DEST"
