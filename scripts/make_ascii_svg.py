"""Turn the Abhi.Designs logo mark into a self-typing two-tone ASCII SVG (white A + red D)."""
import sys, os
import numpy as np
from PIL import Image
from theme import *

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "assets", "logo-source.png")
OUT = os.path.join(ROOT, "ascii-logo.svg")

CROP = (300, 300, 1130, 880)      # just the AD mark (wordmark is real text below)
COLS = 84
RAMP = " .:-=+*#%@"                # sparse -> dense
CW, LH, FS = 7.2, 12.5, 12         # char width, line height, font size

img = Image.open(SRC).convert("RGB").crop(CROP)
w, h = img.size
cell_h_px = (w / COLS) * (LH / CW)
ROWS = round(h / cell_h_px)
small = np.asarray(img.resize((COLS, ROWS), Image.LANCZOS)).astype(float)

W = COLS * CW
H = ROWS * LH + 78
rows = []
for r in range(ROWS):
    runs, cur_col, cur_txt, start = [], None, "", 0
    for c in range(COLS):
        R, G, B = small[r, c]
        v = max(R, G, B) / 255
        if v < 0.14:
            ch, col = " ", None
        else:
            ch = RAMP[min(len(RAMP) - 1, int((v ** 0.75) * (len(RAMP) - 1) + 0.5))]
            col = RED if (R - max(G, B)) > 55 else "#f2f2f2"
        if ch == " " or col != cur_col:
            if cur_txt.strip():
                runs.append((start, cur_txt, cur_col))
            cur_txt, cur_col, start = "", col, c
        if ch != " ":
            if not cur_txt:
                start = c
            cur_txt += ch
            cur_col = col
    if cur_txt.strip():
        runs.append((start, cur_txt, cur_col))
    rows.append(runs)

wordmark_font = font_face("Poppins", 700, "Poppins-Bold.ttf", "Abhi.Designs")
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}">',
       f'<style>{wordmark_font}'
       f'.m{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"DejaVu Sans Mono",monospace;font-size:{FS}px;white-space:pre}}'
       f'.w{{font-family:Poppins,"Segoe UI",Arial,sans-serif;font-weight:700;font-size:38px}}'
       + ('' if STATIC else '.w{opacity:0;animation:f .6s ease 2.4s forwards}@keyframes f{to{opacity:1}}')
       + '</style>',
       f'<rect width="{W:.1f}" height="{H:.1f}" rx="14" fill="{BG}" stroke="{PANEL_BORDER}"/>']

defs = ["<defs>"]
body = []
for r, runs in enumerate(rows):
    y = r * LH
    delay = r * 0.07
    if STATIC:
        defs.append(f'<clipPath id="c{r}"><rect x="0" y="{y:.1f}" width="{W:.1f}" height="{LH}"/></clipPath>')
    else:
        defs.append(f'<clipPath id="c{r}"><rect x="0" y="{y:.1f}" width="0" height="{LH}">'
                    f'<animate attributeName="width" from="0" to="{W:.1f}" begin="{delay:.2f}s" dur="0.55s" fill="freeze"/>'
                    f'</rect></clipPath>')
    g = [f'<g clip-path="url(#c{r})">']
    for start, txt, col in runs:
        g.append(f'<text class="m" x="{start*CW:.1f}" y="{y+LH-3:.1f}" fill="{col}" '
                 f'textLength="{len(txt)*CW:.1f}" lengthAdjust="spacingAndGlyphs">{txt.replace("&","&amp;").replace("<","&lt;")}</text>')
    g.append('</g>')
    body.append("".join(g))
    if not STATIC:   # little red block cursor riding the wipe edge
        body.append(f'<rect y="{y+1:.1f}" width="{CW}" height="{LH-2}" fill="{RED}" opacity="0">'
                    f'<animate attributeName="x" from="0" to="{W:.1f}" begin="{delay:.2f}s" dur="0.55s" fill="freeze"/>'
                    f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.02;0.95;1" begin="{delay:.2f}s" dur="0.55s" fill="freeze"/></rect>')
defs.append("</defs>")
out += defs + body
cy = ROWS * LH + 52
out.append(f'<text class="w" x="{W/2:.1f}" y="{cy:.1f}" text-anchor="middle"><tspan fill="{WHITE}">Abhi.</tspan><tspan fill="{RED}">Designs</tspan></text>')
out.append("</svg>")
open(OUT, "w").write("\n".join(out))
print(f"wrote {OUT}  {W:.0f}x{H:.0f}  rows={ROWS}  (at width 370 -> height {370*H/W:.0f})")
