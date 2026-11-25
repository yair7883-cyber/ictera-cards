# Notes for Claude

## Installing skills

- Before you install any skill (with `npx skills add`, the `find-skills`
  skill, a plugin, or by copying files), read its `SKILL.md` and every script
  it ships. Tell the user what it does, which commands it runs and which sites
  it contacts, and install only after they approve.
- Don't pass `-y` to `npx skills add` for a skill you haven't reviewed.
- Prefer skills from known sources with many installs. Skills from the open
  directory at skills.sh are written by strangers and run with full agent
  permissions.
- Third-party skills in this repo are listed in `.claude/THIRD_PARTY_SKILLS.md`.
