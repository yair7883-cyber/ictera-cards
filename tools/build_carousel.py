"""ICTera carousel builder, per the approved spec (Heebo, 1080x1350 JPG, 5 slides).
Usage: python3 -I tools/build_carousel.py <spec.json> <outdir> [only_slide_number]
spec: {"theme": {...palette...}, "disclaimer": str, "slides": [...]}
Slide types: cover, text, box, stat, cta.  **word** = accent color, \\n = line break.
Layout/typography are fixed; only the accent palette changes per carousel."""
import base64, html, io, json, os, pathlib, subprocess, sys
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
SPEC = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
ONLY = int(sys.argv[3]) if len(sys.argv) > 3 else None
TH = SPEC["theme"]  # a, rgb, glow, dark, halo, ink

FONTS = (HERE / "fonts" / "fonts.css").read_text().replace("url('", f"url('file://{HERE}/fonts/")
logo = Image.open(HERE / "logo.png").convert("RGB").resize((330, 330), Image.LANCZOS)
b = io.BytesIO(); logo.save(b, "PNG"); LOGO = base64.b64encode(b.getvalue()).decode()

def fmt(s):
    parts = html.escape(s).split("**")
    s = "".join(f"<em>{p}</em>" if i % 2 else p for i, p in enumerate(parts))
    return s.replace("\n", "<br>")

CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Heebo,sans-serif;color:#fff;background:radial-gradient(ellipse at 15% 0%,%GLOW% 0%,%DARK% 60%);position:relative}
body:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(%RGB%,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(%RGB%,.05) 2px,transparent 2px);background-size:90px 90px}
body:after{content:"";position:absolute;right:-200px;bottom:-200px;width:900px;height:800px;background:radial-gradient(circle,rgba(%HALO%,.22) 0%,transparent 65%)}
.brand{position:absolute;left:70px;top:100px;font-family:Roboto;font-weight:500;font-size:34px;color:#7f9499;direction:ltr}
.logo{position:absolute;right:70px;top:70px;width:110px;height:110px;border-radius:50%;border:5px solid %A%;box-shadow:0 0 26px rgba(%HALO%,.22);overflow:hidden;background:#000;z-index:2}
.logo img{width:100%;height:100%;object-fit:cover}
.mid{position:absolute;right:80px;left:80px;top:260px;bottom:220px;display:flex;flex-direction:column;justify-content:center;gap:34px;z-index:2}
.mid.center{align-items:center;text-align:center}
h1.huge{font-weight:900;font-size:128px;line-height:1.02;letter-spacing:-1px}
h2{font-weight:900;font-size:84px;line-height:1.08}
em{font-style:normal;color:%A%}
.lead{font-weight:700;font-size:54px;line-height:1.3;color:#d7e3e6}
.body{font-weight:500;font-size:46px;line-height:1.45;color:#d7e3e6}
.body em{font-weight:800}
.stat{font-weight:900;font-size:230px;line-height:1;color:%A%;text-shadow:0 0 50px rgba(%HALO%,.35);direction:ltr}
.box{border:3px solid %A%;border-radius:28px;background:rgba(%RGB%,.08);padding:34px 44px;font-weight:800;font-size:46px;line-height:1.5}
.btn{background:%A%;color:%INK%;font-weight:900;font-size:58px;padding:26px 70px;border-radius:70px;box-shadow:0 0 40px rgba(%HALO%,.3)}
.note{font-weight:500;font-size:40px;color:#7f9499}
.disc{font-size:26px;color:#7f9499;margin-top:30px;font-weight:500}
.swipe{position:absolute;left:70px;bottom:115px;font-weight:800;font-size:36px;color:%A%;z-index:2}
.dots{position:absolute;left:0;right:0;bottom:62px;display:flex;justify-content:center;gap:14px;direction:rtl;z-index:2}
.dot{width:46px;height:8px;border-radius:4px;background:#7f9499;opacity:.45}.dot.on{background:%A%;opacity:1}
.candles{position:absolute;right:90px;bottom:20px}
"""
for k, v in {"%GLOW%": TH["glow"], "%DARK%": TH["dark"], "%RGB%": TH["rgb"], "%HALO%": TH["halo"], "%A%": TH["a"], "%INK%": TH["ink"]}.items():
    CSS = CSS.replace(k, v)

def candles():
    d = [(60,120,230,150,210),(110,90,215,110,190),(160,100,200,120,180),(210,60,190,80,170),(260,40,160,60,140),
         (35,170,250,190,235),(85,140,240,160,225),(135,115,225,135,205),(185,80,210,100,190)]
    g = "".join(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{TH["a"]}" stroke-opacity="{.5 if i%2 else .9}" stroke-width="3"/><rect x="{x-10}" y="{a}" width="20" height="{bb-a}" fill="{TH["a"]}" fill-opacity="{.5 if i%2 else .9}"/>' for i,(x,y1,y2,a,bb) in enumerate(d))
    return f'<svg class="candles" width="290" height="260" viewBox="0 0 290 260">{g}</svg>'

def inner(s):
    k = s["type"]
    if k == "cover":
        return f'<div class="mid"><h1 class="huge">{fmt(s["title"])}</h1><div class="lead">{fmt(s["lead"])}</div></div>' + candles()
    if k == "text":
        return f'<div class="mid"><h2>{fmt(s["title"])}</h2>' + "".join(f'<div class="body">{fmt(l)}</div>' for l in s["lines"]) + "</div>"
    if k == "box":
        items = "<br>".join(f"{i+1}. {fmt(t)}" for i, t in enumerate(s["items"]))
        return f'<div class="mid"><h2>{fmt(s["title"])}</h2><div class="box">{items}</div><div class="note">{fmt(s["note"])}</div></div>'
    if k == "stat":
        return f'<div class="mid center"><div class="stat">{html.escape(s["big"])}</div><h2>{fmt(s["title"])}</h2><div class="box">{fmt(s["box"])}</div></div>'
    if k == "cta":
        return (f'<div class="mid center"><h2>{fmt(s["title"])}</h2><div class="body">{fmt(s["body"])}</div><div class="btn">{fmt(s["button"])}</div>'
                f'<div class="note">{fmt(s["note"])}</div><div class="disc">{html.escape(SPEC["disclaimer"])}</div></div>')

def page(i, n, s):
    dots = "".join(f'<div class="dot {"on" if j == i else ""}"></div>' for j in range(n))
    swipe = '<div class="swipe">החליקו ←</div>' if i < n - 1 else ""
    return (f'<!doctype html><html dir="rtl" lang="he"><meta charset="utf-8"><style>{CSS}</style><body>'
            f'<div class="brand">ICTera</div><div class="logo"><img src="data:image/png;base64,{LOGO}"></div>'
            f'{inner(s)}{swipe}<div class="dots">{dots}</div></body></html>')

slides = SPEC["slides"]; files = []
for i, s in enumerate(slides):
    if ONLY and i + 1 != ONLY: continue
    f = OUT / f"slide{i+1}.html"; f.write_text(page(i, len(slides), s), encoding="utf-8"); files.append(f)
js = OUT / "_shot.js"
js.write_text("""const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const f of process.argv.slice(2)){await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:f.replace('.html','.png')});}await b.close()})()""")
subprocess.run(["node", str(js)] + [str(f.resolve()) for f in files], check=True, env={**os.environ, "NODE_PATH": "/opt/node22/lib/node_modules"})
for f in files:
    png = f.with_suffix(".png"); Image.open(png).convert("RGB").save(f.with_suffix(".jpg"), "JPEG", quality=95, subsampling=0); png.unlink(); f.unlink()
js.unlink(); print("ok", sorted(p.name for p in OUT.glob("slide*.jpg")))
