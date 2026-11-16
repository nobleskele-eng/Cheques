# Weekly table of what the tracked anime editors posted, built from files pull_account.py already wrote. No network.
# usage: python3 -I research/scripts/refs_report.py smokinsasa7 .sadaqatt zrivvn   -> overwrites anime/refs.md
# Reads research/data/<h>_videos.csv (+ <h>_captions.csv when present), research/scratch/<h>.html (followers),
# and anime/references.csv (style label per handle). × = views ÷ that account's median of posts older than 24 h.
import csv, os, statistics, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from account_stats import profile, now  # noqa: E402
ROOT = os.path.dirname(os.path.dirname(HERE))
D = os.path.join(ROOT, 'research', 'data')

def read(path):
    try:
        with open(path, encoding='utf-8-sig') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

styles = {r['handle']: r['role'] for r in read(os.path.join(ROOT, 'anime', 'references.csv'))}
cell = lambda s, n: (s or '').replace('|', '/').replace('\n', ' ')[:n]
out = [f"# Tracked anime editors (refreshed by the Saturday routine)",
       f"Updated {now:%Y-%m-%d} [C pull]. × = views ÷ the account's median (posts older than 24 h). Posts under 24 h old are marked *.", '']
for h in sys.argv[1:]:
    vids = read(os.path.join(D, f'{h}_videos.csv'))
    caps = {r['video_id']: r['caption'] for r in read(os.path.join(D, f'{h}_captions.csv'))}
    p = profile(h)
    if not vids:
        out += [f'## @{h}: no data (pull failed or never ran)', '']
        continue
    for v in vids:
        v['t'] = dt.datetime.strptime(v['posted_utc'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=dt.timezone.utc)
        v['age_h'] = (now - v['t']).total_seconds() / 3600
        v['views'] = int(v['views'])
    settled = [v['views'] for v in vids if v['age_h'] >= 24]
    med = statistics.median(settled) if settled else None
    x = lambda v: f"{v['views'] / med:.1f}×" if med else '-'
    row = lambda v: (f"| {v['t']:%d %b}{'*' if v['age_h'] < 24 else ''} | {v['views']:,} | {x(v)} | {v.get('duration_s', '')} s "
                     f"| {cell(v.get('sound_title'), 40)} | {cell(caps.get(v['video_id']), 90)} |")
    head = '| Posted | Views | × | Length | Sound | Caption |\n|---|---|---|---|---|---|'
    fol = f"{p['followers']:,} followers" if 'followers' in p else 'followers ?'
    out += [f"## @{h} ({styles.get(h, 'style ?')}): {fol}, median {med:,.0f} views, {len(vids)} posts in the pull" if med else f'## @{h}', '']
    recent = sorted([v for v in vids if v['age_h'] < 14 * 24], key=lambda v: v['t'], reverse=True)
    out += ['**Last 14 days**', '', head] + [row(v) for v in recent] if recent else ['**Last 14 days:** no posts']
    best = sorted([v for v in vids if 24 <= v['age_h'] < 60 * 24], key=lambda v: v['views'], reverse=True)[:5]
    if best:
        out += ['', '**Best 5 of the last 60 days**', '', head] + [row(v) for v in best]
    out.append('')
path = os.path.join(ROOT, 'anime', 'refs.md')
open(path, 'w', encoding='utf-8').write('\n'.join(out))
print(f'wrote {path} ({len(sys.argv) - 1} accounts)')
