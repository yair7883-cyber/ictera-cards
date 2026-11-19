"""ICTera carousel builder: 5 slides, 1080x1350 JPG, approved teal style.
Usage: python3 -I tools/build_carousel.py <spec.json> <outdir>
Renders HTML via Playwright chromium (needs node + playwright)."""
import base64, io, json, pathlib, subprocess, sys, html
from PIL import Image, ImageDraw

SPEC = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
LOGO = pathlib.Path(__file__).parent / "logo.png"

def round_logo():
    im = Image.open(LOGO).convert("RGB").resize((240, 240), Image.LANCZOS)
    m = Image.new("L", (240, 240), 0); ImageDraw.Draw(m).ellipse((0, 0, 239, 239), fill=255)
    o = Image.new("RGBA", (240, 240)); o.paste(im, (0, 0), m)
    b = io.BytesIO(); o.save(b, "PNG"); return base64.b64encode(b.getvalue()).decode()
LOGO_B64 = round_logo()

def em(s):  # **word** -> teal
    s = html.escape(s)
    out = ""; parts = s.split("**")
    for i, p in enumerate(parts): out += f'<b class="t">{p}</b>' if i % 2 else p
    return out

TH = SPEC.get("theme", {"a":"#2de0c4","rgb":"45,224,196","glow":"#0f4a50","b1":"#08262c","b2":"#04161b","b3":"#031014","ink":"#04161b","sub":"#d8eeee","mut":"#8fb4b4"})
CSS = """
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;direction:rtl;font-family:'DejaVu Sans','Liberation Sans',sans-serif;color:#fff;
background:radial-gradient(900px 700px at 80% 0%,#0f4a50 0%,transparent 70%),linear-gradient(160deg,#08262c,#04161b 60%,#031014);
position:relative;overflow:hidden}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(45,224,196,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(45,224,196,.06) 1px,transparent 1px);background-size:60px 60px;
-webkit-mask-image:radial-gradient(circle at 50% 40%,#000,transparent 85%)}
.candles{position:absolute;left:20px;bottom:130px;width:300px;height:250px;opacity:.28}
.brand{position:absolute;top:56px;right:64px;font-size:34px;font-weight:700;letter-spacing:1px;color:#fff}
.brand i{color:#2de0c4;font-style:normal}
.logo{position:absolute;top:40px;left:56px;width:110px;height:110px;border-radius:50%;border:3px solid #2de0c4;box-shadow:0 0 30px rgba(45,224,196,.4);filter:brightness(1.5) contrast(1.1)}
.main{position:absolute;inset:200px 80px 220px 80px;display:flex;flex-direction:column;justify-content:center;gap:34px}
h1{font-size:104px;line-height:1.18;font-weight:800}
h2{font-size:78px;line-height:1.2;font-weight:800}
.t{color:#2de0c4;font-weight:inherit}
p{font-size:48px;line-height:1.45;color:#d8eeee}
.big{font-size:300px;font-weight:800;color:#2de0c4;line-height:1;text-align:center;direction:ltr;text-shadow:0 0 60px rgba(45,224,196,.4)}
.frame{border:3px solid #2de0c4;border-radius:36px;padding:44px 40px;background:rgba(45,224,196,.06);display:flex;flex-direction:column;gap:30px}
.row{display:flex;gap:28px;align-items:center;font-size:44px;font-weight:700;line-height:1.3}
.n{flex:none;width:70px;height:70px;border-radius:50%;background:#2de0c4;color:#04161b;font-size:40px;font-weight:800;display:flex;align-items:center;justify-content:center}
.btn{align-self:center;background:#2de0c4;color:#04161b;font-size:56px;font-weight:800;padding:30px 70px;border-radius:70px;box-shadow:0 0 50px rgba(45,224,196,.35)}
.disc{font-size:28px;line-height:1.5;color:#8fb4b4;text-align:center}
.foot{position:absolute;bottom:70px;left:80px;right:80px;display:flex;align-items:center;gap:28px}
.bars{flex:1;display:flex;gap:10px}.bars span{flex:1;height:8px;border-radius:4px;background:rgba(255,255,255,.18)}.bars span.on{background:#2de0c4}
.sw{font-size:32px;color:#2de0c4;font-weight:700}
"""
for k,v in {"#2de0c4":"{a}","45,224,196":"{rgb}","#0f4a50":"{glow}","#08262c":"{b1}","#04161b":"{b2}","#031014":"{b3}","#d8eeee":"{sub}","#8fb4b4":"{mut}"}.items():
    CSS=CSS.replace(k,v.format(**TH)) if False else CSS.replace(k,TH[v[1:-1]])
CANDLES = '<svg class="candles" viewBox="0 0 360 300">' + "".join(
    f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{TH["a"]}" stroke-width="3"/><rect x="{x-14}" y="{a}" width="28" height="{b-a}" fill="{TH["a"] if up else TH["glow"]}" stroke="{TH["a"]}" stroke-width="2"/>'
    for x, y1, y2, a, b, up in [(30,150,290,190,260,0),(90,120,270,160,240,1),(150,100,240,130,210,1),(210,60,200,90,170,0),(270,40,170,60,140,1),(330,10,120,30,100,1)]) + "</svg>"

def slide(i, n, body):
    bars = "".join(f'<span class="{"on" if k <= i else ""}"></span>' for k in range(n))
    sw = '<div class="sw">החליקו ←</div>' if i < n - 1 else ""
    return f"""<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><style>{CSS}</style><body>
<div class="grid"></div>{CANDLES}<div class="brand">IC<i>Tera</i></div><img class="logo" src="data:image/png;base64,{LOGO_B64}">
<div class="main">{body}</div><div class="foot"><div class="bars">{bars}</div>{sw}</div></body></html>"""

def body(s):
    k = s["type"]
    if k == "cover": return f'<h1>{em(s["title"])}</h1><p>{em(s["sub"])}</p>'
    if k == "text": return f'<h2>{em(s["title"])}</h2>' + "".join(f"<p>{em(l)}</p>" for l in s["lines"])
    if k == "list":
        rows = "".join(f'<div class="row"><div class="n">{j+1}</div><div>{em(l)}</div></div>' for j, l in enumerate(s["items"]))
        return f'<h2>{em(s["title"])}</h2><div class="frame">{rows}</div>'
    if k == "big": return f'<h2>{em(s["title"])}</h2><div class="big">{html.escape(s["big"])}</div><p style="text-align:center">{em(s["caption"])}</p>'
    if k == "cta": return f'<h2>{em(s["title"])}</h2><p>{em(s["sub"])}</p><div class="btn">{html.escape(s["button"])}</div><div class="disc">{html.escape(SPEC["disclaimer"])}</div>'

slides = SPEC["slides"]; files = []
for i, s in enumerate(slides):
    f = OUT / f"slide{i+1}.html"; f.write_text(slide(i, len(slides), body(s)), encoding="utf-8"); files.append(f)

shot = OUT / "_shot.js"
shot.write_text("""const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const f of process.argv.slice(2)){await p.goto('file://'+f);await p.screenshot({path:f.replace('.html','.png')});}await b.close()})()""")
subprocess.run(["node", str(shot)] + [str(f.resolve()) for f in files], check=True, env={**__import__("os").environ, "NODE_PATH": "/opt/node22/lib/node_modules"})
for f in files:
    png = f.with_suffix(".png"); Image.open(png).convert("RGB").save(f.with_suffix(".jpg"), "JPEG", quality=92, subsampling=0)
    png.unlink(); f.unlink()
shot.unlink()
print("ok", [p.name for p in sorted(OUT.glob("*.jpg"))])
