# ICTera carousels: handoff (from the cloud builder chat)
Repo: yair7883-cyber/ictera-cards, branch claude/ictera-carousel-guidelines-em8pse. Everything below exists there.

## 1. How carousels were built
- `tools/build_carousel.py <spec.json> <outdir> [slide_number]`: renders 5 slides as 1080x1350 JPG (quality 95) via Playwright chromium (node + NODE_PATH=/opt/node22/lib/node_modules) and Pillow. Needs python3 + Pillow + node playwright.
- Fonts: local `tools/fonts/*.ttf` (Heebo 400/500/700/800/900, Roboto 500) loaded by `tools/fonts/fonts.css`; no network needed. Logo: `tools/logo.png`, cropped round via CSS.
- Spec JSON: `theme` (a, rgb, halo, glow, dark, ink), `disclaimer`, `slides`. Types: cover, text, box, stat, cta. `**word**` = accent colour, `\n` = line break. Layout/typography are fixed to the approved CSS from the video chat.
- Month batch: `plan/december_data.py` (content) + `plan/build_month.py` (writes spec.json, captions.txt, JPGs per folder). Copy for a new month.
- QA: `python3 -I tools/qa_check.py carousels/<month>` (size/format, 5 slides, disclaimer, exact "סקירה", hashtags, forbidden phrases, per-network captions).
- Hebrew punctuation: builder inserts an RLM after Latin words before ? : . , ! (else "CISD?" renders wrong).
- Theme used: teal `#2de0c4`, glow `#0c2a33`, dark `#050c11`, halo `26,190,170`, ink `#04201c`.

## 2. Facebook slideshow reel (~16s with music)
NOT created by me. No reel tool or command was set up here. The existing scheduled FB posts in Metricool are MP4 reels made by the video chat.

## 3. Metricool
I only READ (brand id 7965217, timezone Asia/Jerusalem): getBrandSettings, getScheduledPosts, getBestTimeToPostByNetwork. I never uploaded media or scheduled anything, so I cannot tell you the media/fields flow for new posts. Existing posts show: IG carousel = type POST with 5 JPG URLs on static.metricool.com, autoPublish true;
FB = type REEL with one mp4; TikTok = 5 JPG URLs with tiktokData{privacyOption, title, autoAddMusic:true, photoCoverIndex:0}.
Metricool connector tools: createScheduledPost, createScheduledPostForReview, updateScheduledPost (untested by me).
Scheduled tasks cannot carry connectors (org policy), so bots only run inside an open session that holds them.

## 4. Rules learned from Yair (beyond SPEC.md)
- Each carousel must NOT repeat the previous colour... later reversed: Yair finally said TEAL ONLY for ICTera carousels (gold/purple draft rejected). Teal is the rule.
- New carousels at 10:00 Asia/Jerusalem, Mon/Thu (Metricool benchmark: 10:00 and 18:00 beat 20:00; a 3-week A/B was proposed). Already-scheduled ones stay at 20:00.
- Already scheduled by the video chat, keep: 23.11 FVG, 26.11 sweep, 30.11 post-loss, 3.12 four questions, 7.12 killzone (Israel times: London 09-12, NY 15:30-18:00).
- CTA word exactly "סקירה" (Instagram ReplyRush bot depends on it). Bot is maintained by the video chat; I never touched it.
- Songs: no song was approved or rejected by Yair. Suggestions only, in each captions.txt. IG: Yair adds music himself; Metricool cannot.
- Nothing is published without Yair's "נראה טוב". Yair uploads Instagram himself.
- Open: Yair never approved the 7 December carousels; fate of IG autoPublish (no music) and TikTok short disclaimer was flagged in plan/reports/qa-2026-11-22.md.

## 5. Ideas and finished text
- December set (built, teal, 10:00): 10.12 CISD, 14.12 liquidity, 17.12 daily plan, 21.12 journal, 24.12 quarterly theory, 28.12 three mistakes, 31.12 new-year rules. Full text: `plan/december_data.py`; per-carousel `carousels/2026-12/<date>-<slug>/spec.json` and `captions.txt`.
- Alternates (new design, not used): `carousels/_alternates/` (4 questions, killzone). Killzone times there are New York time, differ from the scheduled 7.12 post.
- Idea queue from the trend scout: `plan/ideas.md`, `plan/trends/2026-11-22.md`.

## 6. Traps
- vidIQ credits are exhausted (paid searches fail).
- Killzone hours: keep one convention (Israel time like the scheduled post).
- Scheduled tasks created from this session fire INTO this session: trig_01NLgXBsAi12XPm2rVjuTobs (QA, Sun-Thu 09:41), trig_016f1jkyBTAZJYBHHJWCyZgC (trend scout, Sun 10:07), trig_01LZXQeTFtQDB6CyaaRtpjeB (improver, Mon 11:17). Disable or recreate them when this session is deleted. trig_01GmA9sRWKTfMLoV1NfJFYnn builds next month's carousels in a fresh session on the 1st at 10:23.
- Chief-of-staff skill points at Windows paths; not usable from the cloud.
