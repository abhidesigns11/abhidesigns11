"""Render data/contributions.json as an animated brand-colored heatmap SVG."""
import json, os, datetime as dt
from theme import *

DATA = os.path.join(ROOT, "data", "contributions.json")
OUT = os.path.join(ROOT, "contrib-heatmap.svg")
W = 860
LEFT, TOP, PITCH, CELL = 40, 44, 15.2, 12

d = json.load(open(DATA)) if os.path.exists(DATA) else {"days": [], "total": 0, "current_streak": 0, "longest_streak": 0}
days = d["days"]
if days:
    first = dt.date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7          # Sunday = 0
else:
    offset = 0
cells = []
for i, day in enumerate(days):
    n = i + offset
    cells.append((n // 7, n % 7, day["level"]))
weeks = max([c[0] for c in cells], default=52) + 1
H = TOP + 7 * PITCH + 62

css = ("text{font-family:Poppins,'Segoe UI',Arial,sans-serif;font-size:11px}")
if not STATIC:
    css += ("@keyframes d{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}"
            ".c{opacity:0;animation:d .4s ease forwards}")
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}">',
       f"<style>{css}</style>",
       f'<rect x=".5" y=".5" width="{W-1}" height="{H-1:.0f}" rx="14" fill="{BG}" stroke="{PANEL_BORDER}"/>']

# month labels
last_m = None
for i, day in enumerate(days):
    dd = dt.date.fromisoformat(day["date"])
    n = i + offset
    if dd.month != last_m and dd.day <= 7 and n % 7 == 0 or (i == 0):
        if dd.month != last_m:
            out.append(f'<text x="{LEFT + (n//7)*PITCH:.1f}" y="{TOP-12}" fill="{MUTED}">{dd.strftime("%b")}</text>')
            last_m = dd.month
for row, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    out.append(f'<text x="10" y="{TOP + row*PITCH + 10:.1f}" fill="{MUTED}">{lab}</text>')

for wk, dow, lvl in cells:
    x, y = LEFT + wk * PITCH, TOP + dow * PITCH
    delay = (wk * 0.018) + dow * 0.03
    style = "" if STATIC else f' class="c" style="animation-delay:{delay:.2f}s"'
    out.append(f'<rect{style} x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[min(lvl,5)]}"/>')
if not cells:   # placeholder grid until the first Action run
    for wk in range(53):
        for dow in range(7):
            out.append(f'<rect x="{LEFT+wk*PITCH:.1f}" y="{TOP+dow*PITCH:.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[0]}"/>')

fy = TOP + 7 * PITCH + 30
if cells:
    foot = f'{d["total"]:,} contributions in the last year  ·  current streak {d["current_streak"]}d  ·  longest {d["longest_streak"]}d'
else:
    foot = "Refreshing... run the Update profile art workflow once"
out.append(f'<text x="{LEFT}" y="{fy:.1f}" fill="{WHITE}" style="font-size:12px;font-weight:500">'
           f'<tspan fill="{RED}">▍</tspan> {foot}</text>')
# legend
lx = W - 40 - 5 * (CELL + 4) - 70
out.append(f'<text x="{lx}" y="{fy:.1f}" fill="{MUTED}">Less</text>')
for i in range(6):
    out.append(f'<rect x="{lx+34+i*(CELL+4)}" y="{fy-CELL+1:.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[i]}"/>')
out.append(f'<text x="{lx+34+6*(CELL+4)+4}" y="{fy:.1f}" fill="{MUTED}">More</text>')
out.append("</svg>")
open(OUT, "w").write("\n".join(out))
print("wrote", OUT)
