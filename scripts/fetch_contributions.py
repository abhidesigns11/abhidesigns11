"""Fetch the public contribution calendar (no token) and write data/contributions.json."""
import json, os, re, datetime as dt
import requests
from bs4 import BeautifulSoup
from theme import USER, ROOT

URL = f"https://github.com/users/{USER}/contributions"
html = requests.get(URL, timeout=30, headers={"User-Agent": "profile-readme-bot"}).text
soup = BeautifulSoup(html, "html.parser")

tips = {}
for t in soup.find_all("tool-tip"):
    m = re.match(r"\s*(No|\d[\d,]*)\s+contribution", t.get_text())
    if m and t.get("for"):
        tips[t["for"]] = 0 if m.group(1) == "No" else int(m.group(1).replace(",", ""))

days = []
for td in soup.select("td.ContributionCalendar-day"):
    if not td.get("data-date"):
        continue
    days.append({"date": td["data-date"],
                 "level": int(td.get("data-level", 0)),
                 "count": tips.get(td.get("id"), 0)})
days.sort(key=lambda d: d["date"])
if not days:
    raise SystemExit("No contribution cells found - GitHub markup may have changed.")

total = sum(d["count"] for d in days)
longest = cur = 0
for d in days:
    cur = cur + 1 if d["count"] else 0
    longest = max(longest, cur)
current = 0
for d in reversed(days):
    if d["count"]:
        current += 1
    elif d["date"] != dt.date.today().isoformat():   # today may still be empty
        break
best = max(days, key=lambda d: d["count"])

os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
with open(os.path.join(ROOT, "data", "contributions.json"), "w") as f:
    json.dump({"user": USER, "total": total, "current_streak": current,
               "longest_streak": longest, "best_day": best, "days": days}, f)
print(f"{len(days)} days, {total} contributions, streak {current}")
