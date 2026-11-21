#!/usr/bin/env python3
"""Render assets/activity.svg — an animated 12-month contribution chart.

Runs daily in GitHub Actions (see .github/workflows/activity.yml).
Uses only the standard library; needs GITHUB_TOKEN in the environment.
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from collections import OrderedDict

LOGIN = os.environ.get("GH_LOGIN", "ghassendev")
OUT = os.environ.get("OUT", os.path.join(os.path.dirname(__file__), "..", "assets", "activity.svg"))

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
      totalCommitContributions totalPullRequestContributions totalIssueContributions
      restrictedContributionsCount
    }
  }
}"""


def fetch():
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-activity"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]["contributionsCollection"]


def streaks(days):
    longest = cur = 0
    for _, c in days:
        cur = cur + 1 if c > 0 else 0
        longest = max(longest, cur)
    current = 0
    for i, (_, c) in enumerate(reversed(days)):
        if c > 0:
            current += 1
        elif i == 0:
            continue  # today may still be empty
        else:
            break
    return current, longest


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def render(cc):
    cal = cc["contributionCalendar"]
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    total = cal["totalContributions"]
    current, longest = streaks(days)
    best_date, best = max(days, key=lambda x: x[1])
    active = sum(1 for _, c in days if c > 0)

    months = OrderedDict()
    for date, c in days:
        k = date[:7]
        months[k] = months.get(k, 0) + c
    months = list(months.items())[-12:]
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]][-52:]

    W, H = 1200, 420
    o = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Contribution activity, last 12 months">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#1a1430"/></linearGradient>
<linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ff5f6d"/><stop offset="1" stop-color="#ffc371"/></linearGradient>
<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5b8cff" stop-opacity=".45"/><stop offset="1" stop-color="#5b8cff" stop-opacity="0"/></linearGradient>
<style>
.t{{font:700 24px 'Segoe UI',Ubuntu,Arial,sans-serif;fill:#e6edf3}}
.s{{font:400 15px 'Segoe UI',Ubuntu,Arial,sans-serif;fill:#8b949e}}
.num{{font:800 34px 'Segoe UI',Ubuntu,Arial,sans-serif;fill:#e6edf3}}
.cap{{font:600 12px 'Segoe UI',Ubuntu,Arial,sans-serif;fill:#8b949e;letter-spacing:1.5px}}
.m{{font:500 12px 'JetBrains Mono',Consolas,monospace;fill:#8b949e}}
.v{{font:700 12px 'JetBrains Mono',Consolas,monospace;fill:#e6edf3}}
.tile{{fill:#ffffff;fill-opacity:.04;stroke:#ffffff;stroke-opacity:.08}}
</style></defs>
<rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="#30363d"/>
<text class="t" x="40" y="52">Activity · last 12 months</text>
<text class="s" x="40" y="78">Updated daily by GitHub Actions · {dt.date.today():%d %b %Y}</text>''']

    tiles = [(f"{total:,}", "CONTRIBUTIONS"), (f"{current}", "DAY STREAK"), (f"{longest}", "BEST STREAK"), (f"{active}", "ACTIVE DAYS")]
    for i, (n, c) in enumerate(tiles):
        x = 40 + i * 140
        o.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".5s" begin="{.15 * i:.2f}s" fill="freeze"/>'
                 f'<rect class="tile" x="{x}" y="104" width="128" height="92" rx="14"/>'
                 f'<text class="num" x="{x + 64}" y="152" text-anchor="middle">{esc(n)}</text>'
                 f'<text class="cap" x="{x + 64}" y="178" text-anchor="middle">{c}</text></g>')
    o.append(f'<text class="s" x="40" y="230">Best day: <tspan fill="#ffc371" font-weight="700">{best}</tspan> contributions on {dt.date.fromisoformat(best_date):%d %b %Y}</text>')

    # weekly sparkline (left, under tiles)
    sx, sy, sw, sh = 40, 275, 540, 110
    mxw = max(weeks) or 1
    pts = [(sx + i * sw / (len(weeks) - 1), sy + sh - sh * v / mxw) for i, v in enumerate(weeks)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"M{sx},{sy + sh} L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" L{sx + sw},{sy + sh} Z"
    length = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** .5 for i in range(len(pts) - 1))
    o.append(f'<text class="cap" x="{sx}" y="{sy - 8}">WEEKLY CONTRIBUTIONS</text>')
    o.append(f'<path d="{area}" fill="url(#area)" opacity="0"><animate attributeName="opacity" from="0" to="1" dur="1s" begin="1.2s" fill="freeze"/></path>')
    o.append(f'<polyline points="{line}" fill="none" stroke="#5b8cff" stroke-width="2.5" stroke-linejoin="round" stroke-dasharray="{length:.0f}" stroke-dashoffset="{length:.0f}">'
             f'<animate attributeName="stroke-dashoffset" from="{length:.0f}" to="0" dur="2s" begin=".3s" fill="freeze"/></polyline>')
    lx, ly = pts[-1]
    o.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="5" fill="#5b8cff" opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".3s" begin="2.2s" fill="freeze"/>'
             f'<animate attributeName="r" values="5;9;5" dur="1.6s" begin="2.3s" repeatCount="indefinite"/></circle>')

    # monthly bars (right)
    bx, by, bh = 640, 120, 230
    bwid = 520 / len(months)
    mxm = max(v for _, v in months) or 1
    o.append(f'<text class="cap" x="{bx}" y="{by - 12}">CONTRIBUTIONS PER MONTH</text>')
    for i, (k, v) in enumerate(months):
        h = max(bh * v / mxm, 3)
        x = bx + i * bwid + 6
        w = bwid - 12
        b = .4 + .08 * i
        month = dt.date.fromisoformat(k + "-01").strftime("%b")
        o.append(f'<rect x="{x:.1f}" y="{by + bh}" width="{w:.1f}" height="0" rx="5" fill="url(#bar)">'
                 f'<animate attributeName="height" from="0" to="{h:.1f}" dur=".9s" begin="{b:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/>'
                 f'<animate attributeName="y" from="{by + bh}" to="{by + bh - h:.1f}" dur=".9s" begin="{b:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>')
        o.append(f'<text class="v" x="{x + w / 2:.1f}" y="{by + bh - h - 8:.1f}" text-anchor="middle" opacity="0">{v}'
                 f'<animate attributeName="opacity" from="0" to="1" dur=".3s" begin="{b + .8:.2f}s" fill="freeze"/></text>')
        o.append(f'<text class="m" x="{x + w / 2:.1f}" y="{by + bh + 22}" text-anchor="middle">{month}</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    svg = render(fetch())
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT}")
