# -*- coding: utf-8 -*-
"""QA bot (deterministic part). Usage: python3 -I tools/qa_check.py carousels/2026-12 [more dirs]
Checks every carousel folder against the ICTera brief. Exit code 1 if any FAIL."""
import json, pathlib, re, sys
from PIL import Image
DISC = "תוכן לימודי בלבד, לא ייעוץ השקעות. מסחר בחוזים עתידיים כרוך בסיכון גבוה."
BAD = ["מובטח","בלי סיכון","ללא סיכון","בטוח ב","הקהילה הכי חזקה","100%","₪","$","ערובה","ללא הפסד","רווח של"]
fails = warns = 0
def fail(d, m):
    global fails; fails += 1; print(f"FAIL {d.name}: {m}")
def warn(d, m):
    global warns; warns += 1; print(f"WARN {d.name}: {m}")
for root in sys.argv[1:]:
    for d in sorted(p for p in pathlib.Path(root).iterdir() if p.is_dir()):
        if not (d / "spec.json").exists(): continue
        for i in range(1, 6):
            f = d / f"slide{i}.jpg"
            if not f.exists(): fail(d, f"missing slide{i}.jpg"); continue
            im = Image.open(f)
            if im.format != "JPEG" or im.size != (1080, 1350): fail(d, f"slide{i} must be JPEG 1080x1350, is {im.format} {im.size}")
        spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
        sl = spec["slides"]
        if len(sl) != 5: fail(d, "needs 5 slides")
        if sl[-1]["type"] != "cta" or DISC not in json.dumps(spec, ensure_ascii=False).replace("\\u200f", ""): fail(d, "last slide must be CTA with disclaimer")
        if "סקירה" not in sl[-1].get("button", ""): fail(d, 'CTA button must contain exactly "סקירה"')
        for s in sl:
            if s["type"] == "text" and len(s["lines"]) > 3: fail(d, "text slide has more than 3 body lines")
        cap = (d / "captions.txt").read_text(encoding="utf-8")
        parts = re.split(r"=== (.+?) ===", cap)
        secs = {parts[k]: parts[k+1].strip() for k in range(1, len(parts) - 1, 2)}
        for need in ["אינסטגרם", "פייסבוק", "טיקטוק"]:
            if need not in secs: fail(d, f"caption section missing: {need}")
        if len(set(secs.get(k, k) for k in ["אינסטגרם", "פייסבוק", "טיקטוק"])) < 3: fail(d, "captions must differ per network")
        for k in ["אינסטגרם", "פייסבוק"]:
            t = secs.get(k, ""); tags = re.findall(r"#\S+", t)
            if len(tags) > 5: fail(d, f"{k}: more than 5 hashtags")
            if DISC not in t: fail(d, f"{k}: disclaimer missing")
            if 'תגיבו "סקירה"' not in t: fail(d, f'{k}: CTA "סקירה" missing')
            if "?" not in t: warn(d, f"{k}: no question for comments")
            body = [l for l in t.splitlines() if l.strip() and not l.startswith("#")]
            if not (5 <= len(body) <= 10): warn(d, f"{k}: {len(body)} non-hashtag lines (expected hook + 3-6 + CTA + disclaimer)")
            lines = t.splitlines()
            if not (lines[-1].startswith("#") and re.fullmatch(r"(#[A-Za-z]+\s*)+", lines[-1])): fail(d, f"{k}: English hashtags must be on a separate last line")
        tt = secs.get("טיקטוק", "")
        if "כותרת:" not in tt: fail(d, "TikTok title missing")
        if len(re.findall(r"#\S+", tt)) > 4: fail(d, "TikTok: more than 4 hashtags")
        if "_" in "".join(re.findall(r"#\S+", cap)): fail(d, "hashtags must not contain underscore")
        full = cap + json.dumps(spec, ensure_ascii=False)
        for b in BAD:
            if b in full: fail(d, f"forbidden phrase: {b}")
        if "שיר" not in cap: warn(d, "no song suggestion")
print(f"\nQA done: {fails} fail, {warns} warn"); sys.exit(1 if fails else 0)
