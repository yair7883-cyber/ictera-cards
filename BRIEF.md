# ICTera carousels: working brief (for the monthly build)

Role: build carousels only and submit to Yair for approval. Never upload, schedule, or touch accounts.
Video chat schedules TikTok/Facebook in Metricool after Yair's "נראה טוב". Yair uploads Instagram himself.
Nothing goes out without Yair's approval of the final version.

Cadence: Mondays and Thursdays 20:00 (Asia/Jerusalem). No posts from Friday 14:00 until Saturday night,
nor on Yom Kippur, Memorial Day, Holocaust Day, or 7 October.

Per carousel: 5 JPG 1080x1350 (cover, 3 teaching, CTA), captions for IG, FB, TikTok + TikTok title, song suggestion.
Design: approved teal style, Heebo, fixed layout (tools/build_carousel.py). Teal only (#2de0c4), decided by Yair.
Text: spoken Hebrew, short; hook teaches or creates tension; no certainty, no profit promises, no profit amounts,
no "strongest community". CTA: comment "סקירה" (exact word; the ReplyRush bot on Instagram depends on it).
Disclaimer on the last slide and in every caption: "תוכן לימודי בלבד, לא ייעוץ השקעות. מסחר בחוזים עתידיים כרוך בסיכון גבוה."
Captions: separate per network. IG/FB: line 1 hook, 3-6 short lines, real question, CTA, disclaimer, up to 5 hashtags
(Hebrew without underscores, English on a separate last line). TikTok: 1-2 lines, up to 4 hashtags, short title (required).
Music is mandatory for TikTok and Instagram; propose a song/mood.

Monthly workflow: copy plan/december_data.py to plan/<month>_data.py, write the month's carousels (avoid repeating
published topics), run plan/build_month.py (adjust month/dates), review the overview sheet, push to the branch, and
present the sheet to Yair. Do not open a PR unless asked.
Already covered topics: 1% risk, FVG, sweep, post-loss trade, 4 questions, CISD, killzone, liquidity, daily plan,
journal, quarterly theory, recurring mistakes, new-year rules.
