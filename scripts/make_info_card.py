"""Brand-styled info card (neofetch-style). Edit CONTENT below, then run this script."""
import os
from theme import *

OUT = os.path.join(ROOT, "info-card.svg")
W, H = 490, 308          # H matches the portrait's displayed height at width 370

TITLE = "abhi@designs ~ whoami"
CONTENT = [               # (key, value)  <- edit these
    ("Name",     "Abhi"),
    ("Role",     "Developer + Designer"),
    ("Brand",    "Abhi.Designs  (@abhi.designs_)"),
    ("Stack",    "PHP · MySQL · Firebase · PWA · Capacitor"),
    ("Building", "Invoice Flex · NexusFlow"),
    ("Focus",    "Logo redesigns for small brands"),
    ("Contact",  "github.com/" + USER),
]

ALL_TEXT = TITLE + "".join(k + v for k, v in CONTENT) + "$ _:0123456789"
faces = font_face("Poppins", 500, "Poppins-Medium.ttf", ALL_TEXT) + \
        font_face("Poppins", 700, "Poppins-Bold.ttf", ALL_TEXT)

css = (faces +
       ".t{font-family:Poppins,'Segoe UI',Arial,sans-serif;font-size:14px;font-weight:500}"
       ".k{fill:%s;font-weight:700}.v{fill:%s}.bar{fill:%s}.ti{fill:%s;font-size:12px}" % (RED, WHITE, "#141414", MUTED))
if not STATIC:
    css += ("@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}"
            ".ln{opacity:0;animation:in .45s ease forwards}"
            "@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:bl 1s steps(1) infinite}")

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
       f"<style>{css}</style>",
       f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{BG}" stroke="{PANEL_BORDER}"/>',
       f'<path d="M1 14a13 13 0 0 1 13-13h{W-28}a13 13 0 0 1 13 13v22H1z" class="bar"/>',
       f'<circle cx="22" cy="19" r="5" fill="{RED}"/><circle cx="40" cy="19" r="5" fill="{WHITE}"/><circle cx="58" cy="19" r="5" fill="#444"/>',
       f'<text class="t ti" x="{W/2}" y="23" text-anchor="middle">{TITLE}</text>',
       f'<line x1="1" x2="{W-1}" y1="36" y2="36" stroke="{PANEL_BORDER}"/>']

y0, step = 74, 31
for i, (k, v) in enumerate(CONTENT):
    d = 0.25 + i * 0.22
    style = "" if STATIC else f' style="animation-delay:{d:.2f}s"'
    out.append(f'<g class="ln"{style} {"" if not STATIC else "opacity=\"1\""}>'
               f'<text class="t k" x="28" y="{y0+i*step}">{k}</text>'
               f'<text class="t v" x="128" y="{y0+i*step}">{v}</text></g>')
py = y0 + len(CONTENT) * step + 2
out.append(f'<text class="t" x="28" y="{py}" fill="{RED}">$</text>'
           f'<rect class="cur" x="44" y="{py-13}" width="9" height="16" fill="{WHITE}"/>')
out.append("</svg>")
open(OUT, "w").write("\n".join(out))
print("wrote", OUT)
