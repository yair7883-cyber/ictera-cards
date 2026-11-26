#!/usr/bin/env bash
# Re-install the third-party Claude skills listed in .claude/THIRD_PARTY_SKILLS.md
# from their newest GitHub versions. Run from the repository root, then commit.
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 --filter=blob:limit=2m https://github.com/heygen-com/hyperframes.git "$TMP/hyperframes"
bash "$ROOT/tools/install-claude-skills.sh" "$TMP" "$ROOT/.claude"
echo "hyperframes $(git -C "$TMP/hyperframes" rev-parse --short HEAD)"
echo "Update the commit column in .claude/THIRD_PARTY_SKILLS.md, then commit."
