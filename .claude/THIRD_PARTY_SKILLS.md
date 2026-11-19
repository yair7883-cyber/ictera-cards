# Third-party Claude skills in this repo

The skills under `.claude/skills/` and the subagents under `.claude/agents/`
come from two open-source projects. Claude Code loads them automatically in
every session on this repository.

| Project | Source | Commit | Licence | What it adds |
| --- | --- | --- | --- | --- |
| Claude Ads v2.1.0 | github.com/AgriciDaniel/claude-ads | `fc3908e` (2026-10-17) | MIT (`skills/ads/LICENSE`) | `ads` (the conductor) and 33 `ads-*` skills for paid media: audits, plans, budgets, creative, tracking, per-platform reviews. 25 subagents in `agents/`. |
| HyperFrames | github.com/heygen-com/hyperframes | `3f3a620` (2026-11-19) | Apache-2.0 (`skills/hyperframes/LICENSE`) | `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `figma`, `slideshow`, `reverse-any-video`, `remotion-to-hyperframes`, `style-sampling`: making and rendering videos from HTML. |

The files are copied unchanged, in the layout each project's own installer
uses. To update them to the newest versions, run
`bash tools/update-claude-skills.sh` from the repository root and commit.

Notes:

- `ads` scripts need the Python packages in `skills/ads/requirements.txt`.
- HyperFrames runs its CLI with Node through `npx hyperframes`, and its skills
  run `npx hyperframes events` to send the skill's name with the CLI's usage
  telemetry; the CLI honours its opt-out.
- Three references in the claude-ads skills point at repository paths:
  `skills/ads-meta/SKILL.md` means `.claude/skills/ads-meta/SKILL.md`, and
  `scripts/fetch_page.py` in `ads-landing` means
  `.claude/skills/ads/scripts/fetch_page.py`.
