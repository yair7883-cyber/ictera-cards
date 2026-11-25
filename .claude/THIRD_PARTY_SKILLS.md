# Third-party Claude skills in this repo

The skills under `.claude/skills/` and the subagents under `.claude/agents/`
come from three open-source projects. Claude Code loads them automatically in
every session on this repository.

| Project | Source | Commit | Licence | What it adds |
| --- | --- | --- | --- | --- |
| Claude Ads v2.1.0 | github.com/AgriciDaniel/claude-ads | `fc3908e` (2026-10-17) | MIT (`skills/ads/LICENSE`) | `ads` (the conductor) and 33 `ads-*` skills for paid media: audits, plans, budgets, creative, tracking, per-platform reviews. 25 subagents in `agents/`. |
| HyperFrames | github.com/heygen-com/hyperframes | `3f3a620` (2026-11-19) | Apache-2.0 (`skills/hyperframes/LICENSE`) | `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `figma`, `slideshow`, `reverse-any-video`, `remotion-to-hyperframes`, `style-sampling`: making and rendering videos from HTML. |
| Skills CLI | github.com/vercel-labs/skills | `57217cf` (2026-11-25) | MIT (`skills/find-skills/LICENSE`) | `find-skills`: searches the open skills directory at skills.sh with `npx skills find` and installs with `npx skills add`. One instruction file, no scripts. |

The files are copied unchanged, in the layout each project's own installer
uses. To update them to the newest versions, run
`bash tools/update-claude-skills.sh` from the repository root and commit.

Notes:

- `ads` scripts need the Python packages in `skills/ads/requirements.txt`.
- HyperFrames runs its CLI with Node through `npx hyperframes`, and its skills
  run `npx hyperframes events` to send the skill's name with the CLI's usage
  telemetry; the CLI honours its opt-out.
- `find-skills` runs the `skills` CLI from npm (`npx skills`, about 0.7MB).
  The CLI sends install counts to skills.sh; `DISABLE_TELEMETRY=1` or
  `DO_NOT_TRACK=1` turns that off. Its step 6 installs with `-y`, which skips
  the confirmation; `CLAUDE.md` in the repository root asks for a review first.
- Three references in the claude-ads skills point at repository paths:
  `skills/ads-meta/SKILL.md` means `.claude/skills/ads-meta/SKILL.md`, and
  `scripts/fetch_page.py` in `ads-landing` means
  `.claude/skills/ads/scripts/fetch_page.py`.
