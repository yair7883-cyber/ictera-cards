# -*- coding: utf-8 -*-
import json, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from december_data import C, DISC
ROOT = pathlib.Path(__file__).resolve().parent.parent
TEAL = {"a":"#2de0c4","rgb":"45,224,196","halo":"26,190,170","glow":"#0c2a33","dark":"#050c11","ink":"#04201c"}
for date, slug, slides, ig, fb, q, tt_t, tt_l, tags, song in C:
    d = ROOT / "carousels" / "2026-12" / f"{date[5:]}-{slug}"; d.mkdir(parents=True, exist_ok=True)
    (d / "spec.json").write_text(json.dumps({"theme":TEAL,"disclaimer":DISC,"slides":slides}, ensure_ascii=False, indent=1), encoding="utf-8")
    cta = 'תגיבו "סקירה" ונשלח לכם בפרטי את הסקירה והקהילה.'
    he = tags; en = "#ICT #NQ"
    txt = (f"פרסום: {date} ב-10:00\n\n=== אינסטגרם ===\n{ig[0]}\n" + "\n".join(ig[1:]) + f"\n{q}\n{cta}\n{DISC}\n{he}\n{en}\n\n"
           f"=== פייסבוק ===\n{fb[0]}\n" + "\n".join(fb[1:]) + f"\n{q}\n{cta}\n{DISC}\n{he}\n{en}\n\n"
           f"=== טיקטוק ===\nכותרת: {tt_t}\nכיתוב: {tt_l} {cta.split(' ונשלח')[0]} #מסחריומי #נאסדק #ICT\n\n=== שיר (הצעה) ===\n{song}\n")
    (d / "captions.txt").write_text(txt, encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(ROOT/"tools"/"build_carousel.py"), str(d/"spec.json"), str(d)], check=True, stdout=subprocess.DEVNULL)
print("built", len(C))
