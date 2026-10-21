import json, sys, datetime as dt
UTC = dt.timezone.utc
data_dir, out = sys.argv[1], sys.argv[2]
W, H = 760, 420; L, R, TOP, BOT = 64, 168, 92, 44
x0 = dt.datetime(2026, 6, 1, tzinfo=UTC).timestamp(); x1 = dt.datetime(2026, 10, 22, tzinfo=UTC).timestamp()
ymax = 400e6
X = lambda t: L + (t - x0) / (x1 - x0) * (W - L - R)
Y = lambda v: H - BOT - v / ymax * (H - TOP - BOT)
pw = json.load(open(f'{data_dir}/piecewise.json'))
series = [('elsewhere557', 'var(--series-2)'), ('someplace505', 'var(--series-1)')]
parts = []
# gridlines + y ticks
for v in [0, 100e6, 200e6, 300e6, 400e6]:
    y = Y(v); cls = 'axis' if v == 0 else 'grid'
    parts.append(f'<line class="{cls}" x1="{L}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}"/>')
    parts.append(f'<text class="tick" x="{L-8}" y="{y+4:.1f}" text-anchor="end">{int(v/1e6)}{"M" if v else ""}</text>')
# x ticks (month starts)
for m in [6, 7, 8, 9, 10]:
    t = dt.datetime(2026, m, 1, tzinfo=UTC).timestamp(); x = X(t)
    parts.append(f'<text class="tick" x="{x:.1f}" y="{H-BOT+20}" text-anchor="middle">{dt.date(2026, m, 1):%b}</text>')
ends = []
for h, col in series:
    pts = json.load(open(f'{data_dir}/{h}.daily.json'))
    first = json.load(open(f'{data_dir}/{h}.items.json'))[0]['createTime']
    coords = [(X(first), Y(0))] + [(X(p['ts']), Y(p['views'])) for p in pts]
    d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in coords)
    parts.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    # takeoff marker (piecewise break1 on views)
    bd = pw[h]['views']['break1']; bt = dt.datetime.fromisoformat(bd).replace(tzinfo=UTC).timestamp() + 86400
    bp = min(pts, key=lambda p: abs(p['ts'] - bt))
    bx, by = X(bp['ts']), Y(bp['views'])
    parts.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="4" fill="{col}" stroke="var(--surface-1)" stroke-width="2"/>')
    lbl = f'{dt.date.fromisoformat(bd):%b} {dt.date.fromisoformat(bd).day}'
    parts.append(f'<text class="note" x="{bx-8:.1f}" y="{by-10:.1f}" text-anchor="end">{lbl}</text>')
    ex, ey = coords[-1]
    parts.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{col}" stroke="var(--surface-1)" stroke-width="2"/>')
    ends.append((h, ex, ey, pts[-1]['views']))
for h, ex, ey, v in ends:
    parts.append(f'<text class="label" x="{ex+10:.1f}" y="{ey-2:.1f}">@{h}</text>')
    parts.append(f'<text class="value" x="{ex+10:.1f}" y="{ey+14:.1f}">{v/1e6:.1f}M views</text>')
# legend
lx = L
for h, col in series:
    parts.append(f'<line x1="{lx}" x2="{lx+18}" y1="66" y2="66" stroke="{col}" stroke-width="2" stroke-linecap="round"/>')
    parts.append(f'<text class="legend" x="{lx+24}" y="70">@{h}</text>')
    lx += 150
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Cumulative views by post date, @elsewhere557 vs @someplace505</title>
<desc id="d">Both accounts were flat until takeoff: elsewhere557 on Aug 8 2026 (346.6M cumulative views by Oct 21), someplace505 on Aug 31 2026 (107.2M by Oct 21).</desc>
<style>
svg {{ --surface-1:#fcfcfb; --ink-1:#0b0b0b; --ink-2:#52514e; --muted:#898781; --grid:#e1e0d9; --axis:#c3c2b7; --series-1:#2a78d6; --series-2:#eb6834; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
@media (prefers-color-scheme: dark) {{ svg {{ --surface-1:#1a1a19; --ink-1:#f0efec; --ink-2:#c3c2b7; --muted:#898781; --grid:#2c2c2a; --axis:#383835; --series-1:#3987e5; --series-2:#d95926; }} }}
.bg {{ fill: var(--surface-1); }}
.grid {{ stroke: var(--grid); stroke-width: 1; }}
.axis {{ stroke: var(--axis); stroke-width: 1; }}
.tick {{ fill: var(--muted); font-size: 12px; font-variant-numeric: tabular-nums; }}
.title {{ fill: var(--ink-1); font-size: 16px; font-weight: 600; }}
.sub {{ fill: var(--ink-2); font-size: 12px; }}
.legend, .label {{ fill: var(--ink-1); font-size: 13px; }}
.value {{ fill: var(--ink-2); font-size: 12px; }}
.note {{ fill: var(--ink-2); font-size: 11px; }}
</style>
<rect class="bg" width="{W}" height="{H}" rx="8"/>
<text class="title" x="{L}" y="28">Cumulative views by post date</text>
<text class="sub" x="{L}" y="46">Lifetime views of all videos posted up to each day · dot = takeoff date (piecewise fit) · data pulled 2026-10-21</text>
{chr(10).join(parts)}
</svg>
'''
open(out, 'w').write(svg)
print('wrote', out, len(svg))
