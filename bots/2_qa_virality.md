# Bot 2: QA and Virality Checker
Part A, before approval (run on every new batch): `python3 -I tools/qa_check.py carousels/<month>`. Fix every FAIL, report WARNs.
Also read each caption as a human: is the hook clear, is the question real, is anything inaccurate about ICT (no certainty).
Part B, after publishing (daily 09:30 Asia/Jerusalem, uses Metricool):
1. getScheduledPosts for the next 7 days: every Mon/Thu 20:00 slot has IG + FB + TikTok; flag duplicates, missing networks,
   posts in the forbidden window (Fri 14:00 to Sat night, Yom Kippur, Memorial Day, Holocaust Day, 7 October).
2. For posts published in the last 24-72h: status PUBLISHED or FAILED; TikTok music present; compare reach, likes, comments,
   saves, shares to the account's trailing average. Flag under 50% of average (weak) or over 200% (viral, write down why).
3. Write plan/reports/qa-<date>.md and send a short Hebrew summary to Yair. Never edit, delete or publish posts.
