"""ICTera card builder, high quality (2160x2160 PNG).

Usage: python3 -I build_card_hq.py <logo_png> <spec_json> <out_png>
spec_json: {"sentence": [l1, l2], "explain": [l1, l2, l3]}

Flat #161617 background, logo centered at 480x480 (in a 1080 canvas) with no blur
mask, logo cleaned with LUT (v-55)*255/145 to remove the gray halo.
"""
import base64
import html
import io
import json
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageFont

LOGO = pathlib.Path(sys.argv[1])
SPEC = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
OUT = pathlib.Path(sys.argv[3])

FONT = "Liberation Sans, DejaVu Sans, sans-serif"
TEAL = "#5fe3d4"
BG = "#161617"


def clean_logo(path):
    im = Image.open(path).convert("RGB")
    im = im.resize((960, 960), Image.LANCZOS)  # 2x the 480 slot, matches 2160 output
    a = np.asarray(im).astype(np.float32)
    a = np.clip((a - 55.0) * 255.0 / 145.0, 0, 255)
    # lift pure black to the background colour so no dark square shows
    bg = np.array([0x16, 0x16, 0x17], dtype=np.float32)
    a = np.maximum(a, bg)
    # the logo file has stray bits (a teal spark and a gray fragment) below the
    # logo body; the old blur mask hid them, so clear the bottom rows instead
    a[800:, :, :] = bg
    out = Image.fromarray(a.astype(np.uint8), "RGB")
    buf = io.BytesIO()
    out.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


LOGO_B64 = clean_logo(LOGO)

DEFS = f"""
<defs>
  <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/>
    <stop offset="0.48" stop-color="#c7c9cc"/>
    <stop offset="0.52" stop-color="#8b8e93"/>
    <stop offset="1" stop-color="#e4e6e8"/>
  </linearGradient>
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
    f'<rect width="1080" height="1080" fill="{BG}"/>',
    '<rect x="30" y="30" width="1020" height="1020" rx="36" fill="none" '
    'stroke="#ffffff" stroke-opacity="0.14" stroke-width="3"/>',
    f'<image xlink:href="data:image/png;base64,{LOGO_B64}" x="300" y="70" width="480" height="480"/>',
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
