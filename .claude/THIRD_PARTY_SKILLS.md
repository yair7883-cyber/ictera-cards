# Third-party Claude skills in this repo

The skills under `.claude/skills/` come from one open-source project. Claude
Code loads them automatically in every session on this repository.

| Project | Source | Commit | Licence | What it adds |
| --- | --- | --- | --- | --- |
| HyperFrames | github.com/heygen-com/hyperframes | `3f3a620` (2026-11-19) | Apache-2.0 (`skills/hyperframes/LICENSE`) | `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `figma`, `slideshow`, `reverse-any-video`, `remotion-to-hyperframes`, `style-sampling`: making and rendering videos from HTML. |

The files are copied unchanged, in the layout the project's own installer
uses. To update them to the newest version, run
`bash tools/update-claude-skills.sh` from the repository root and commit.

Notes:

- HyperFrames runs its CLI with Node through `npx hyperframes`, and its skills
  run `npx hyperframes events` to send the skill's name with the CLI's usage
  telemetry; the CLI honours its opt-out.
- The Claude Ads skills (github.com/AgriciDaniel/claude-ads) were removed to
  cut the token cost of loading their 34 skills and 25 subagents in every
  session. To bring them back, restore them from git history.
