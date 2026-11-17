"""ICTera card builder, high quality (2160x2160 PNG).

Usage: python3 -I build_card_hq.py <logo_png> <spec_json> <out_png>
spec_json: {"sentence": [l1, l2], "explain": [l1, l2, l3]}  (optional "style": "A" removes the candles backdrop)

Design = the approved ICTera look (Yair's sample): radial charcoal background with a soft
centre glow, a faint candlestick-chart backdrop (Japanese candles, rising to the right, behind
the text; on by default), the original logo at 580px (in a 1080 canvas) fading into the background through a
radial mask, chrome headline, teal underline with glow, soft-white explanation, teal tagline.
The SVG is laid out on a 1080 canvas and rasterised at 2160. The logo is pre-upscaled with
LANCZOS so it stays sharp at 2160.
"""
import base64
import html
import io
import json
import pathlib
import subprocess
import sys
import tempfile

from PIL import Image, ImageFilter, ImageFont

LOGO = pathlib.Path(sys.argv[1])
SPEC = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
OUT = pathlib.Path(sys.argv[3])

FONT = "Liberation Sans, DejaVu Sans, sans-serif"
TEAL = "#5fe3d4"


def logo_b64():
    im = Image.open(LOGO).convert("RGB")
    im = im.resize((1160, 1160), Image.LANCZOS)  # 580 slot x2, matches the 2160 output
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=45, threshold=2))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


LOGO_B64 = logo_b64()

DEFS = """
<defs>
  <radialGradient id="bg" gradientUnits="userSpaceOnUse" cx="540" cy="360" r="820">
    <stop offset="0" stop-color="#2b2b2d"/>
    <stop offset="1" stop-color="#0c0c0d"/>
  </radialGradient>
  <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/>
    <stop offset="0.48" stop-color="#c7c9cc"/>
    <stop offset="0.52" stop-color="#8b8e93"/>
    <stop offset="1" stop-color="#e4e6e8"/>
  </linearGradient>
  <radialGradient id="fadeg" gradientUnits="userSpaceOnUse" cx="540" cy="305" r="290">
    <stop offset="0" stop-color="#ffffff"/>
    <stop offset="0.72" stop-color="#ffffff"/>
    <stop offset="1" stop-color="#000000"/>
  </radialGradient>
  <mask id="fade" maskUnits="userSpaceOnUse" x="0" y="0" width="1080" height="1080">
    <rect width="1080" height="1080" fill="url(#fadeg)"/>
  </mask>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="10"/>
  </filter>
</defs>
"""


def text(y, s, size, fill, weight=400, extra=""):
    return (
        f'<text x="540" y="{y}" text-anchor="middle" direction="rtl" '
        f'font-family="{FONT}" font-weight="{weight}" font-size="{size}" '
        f'fill="{fill}" {extra}>{s}</text>'
    )


def candles():
    data = [
        (90, 760, 960, 800, 920), (170, 720, 940, 760, 900), (250, 750, 920, 780, 880),
        (330, 690, 900, 720, 860), (410, 670, 880, 710, 830), (490, 700, 860, 720, 840),
        (570, 640, 830, 670, 790), (650, 610, 810, 650, 770), (730, 630, 780, 660, 750),
        (810, 590, 770, 620, 730), (890, 560, 750, 590, 710), (970, 520, 730, 550, 690),
    ]
    out = ['<g opacity="0.16" stroke-width="4">']
    for i, (x, wt, wb, bt, bb) in enumerate(data):
        col = TEAL if i % 2 == 0 else "#d5d7da"
        out.append(
            f'<line x1="{x}" y1="{wt}" x2="{x}" y2="{wb}" stroke="{col}"/>'
            f'<rect x="{x - 18}" y="{bt}" width="36" height="{bb - bt}" fill="{col}"/>'
        )
    out.append("</g>")
    return "".join(out)


def check_width(lines, size, bold, limit):
    f = None
    for path in (
        "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % ("Bold" if bold else "Regular"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
    ):
        try:
            f = ImageFont.truetype(path, size)
            break
        except OSError:
            f = None
    if f is None:
        return
    for line in lines:
        w = f.getlength(line)
        if w > limit:
            sys.exit(f"LINE TOO WIDE ({w:.0f}px > {limit}px): {line!r} - shorten it")


s_lines = SPEC["sentence"]
e_lines = SPEC["explain"]
check_width(s_lines, 68, True, 900)
check_width(e_lines, 33, False, 900)
s_lines = [html.escape(x) for x in s_lines]
e_lines = [html.escape(x) for x in e_lines]

body = [
    '<rect width="1080" height="1080" fill="url(#bg)"/>',
    candles() if str(SPEC.get("style", "B")).upper() != "A" else "",
    '<rect x="30" y="30" width="1020" height="1020" rx="36" fill="none" '
    'stroke="#ffffff" stroke-opacity="0.14" stroke-width="3"/>',
    f'<image xlink:href="data:image/png;base64,{LOGO_B64}" '
    'x="250" y="20" width="580" height="580" mask="url(#fade)"/>',
]
y = 665
for line in s_lines:
    body.append(text(y, line, 68, "url(#chrome)", 700))
    y += 85
body.append(f'<rect x="430" y="783" width="220" height="6" rx="3" fill="{TEAL}" filter="url(#blur)" opacity="0.8"/>')
body.append(f'<rect x="430" y="783" width="220" height="6" rx="3" fill="{TEAL}"/>')
y = 850
for line in e_lines:
    body.append(text(y, line, 33, "#d3d6d9", 400, 'fill-opacity="0.9"'))
    y += 46
body.append(text(992, "מסחר יומי · חוזים עתידיים · מניות", 26, TEAL, 400, 'letter-spacing="2"'))
body.append(text(1026, "תוכן לימודי בלבד, לא ייעוץ השקעות", 21, "#9a9da2"))

svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    'width="1080" height="1080" viewBox="0 0 1080 1080">' + DEFS + "".join(body) + "</svg>"
)

with tempfile.TemporaryDirectory() as td:
    svg_path = pathlib.Path(td) / "card.svg"
    svg_path.write_text(svg, encoding="utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["rsvg-convert", "-w", "2160", "-h", "2160", str(svg_path), "-o", str(OUT)],
        check=True,
    )

im = Image.open(OUT)
print("size", im.size, "mode", im.mode, "bytes", OUT.stat().st_size)
