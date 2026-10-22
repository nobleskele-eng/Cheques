#!/usr/bin/env python3
"""Rebuild research/data/proven_sounds.csv from {account}_videos.csv + _sounds.csv.
usage: python3 research/scripts/proven_sounds.py [data_dir] [out_csv]
Written 2026-10-22 (the original script was never committed); reproduces the 2026-10-21 CSV.

Population: videos from the active period (>= 2026-08-24) of someplace505 and elsewhere557, own-upload
sounds excluded only if used once. A sound is listed when the network used it 3+ times.
relative views = video views / median views of that account's videos posted the same Monday-week.
proven            = 3+ uses, median relative views >= 2, and >= 60% of uses beat the week median.
likely_paid_promo = official library track, 8+ uses, median relative views < 1.
"""
import csv, os, sys, statistics as st, datetime as dt
from collections import defaultdict
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = sys.argv[1] if len(sys.argv) > 1 else f'{R}/data'
OUT = sys.argv[2] if len(sys.argv) > 2 else f'{R}/data/proven_sounds.csv'
ACCTS, START, MONTH = ['someplace505', 'elsewhere557'], '2026-08-24', '2026-10'
rd = lambda p: list(csv.DictReader(open(p, encoding='utf-8')))
wk = lambda s: (dt.date.fromisoformat(s[:10]) - dt.timedelta(days=dt.date.fromisoformat(s[:10]).weekday()))
uses = defaultdict(list)
for a in ACCTS:
    vids = [v for v in rd(f'{D}/{a}_videos.csv') if v['posted_utc'] >= START]
    byw = defaultdict(list)
    for v in vids: byw[wk(v['posted_utc'])].append(int(v['views']))
    med = {k: st.median(x) for k, x in byw.items()}
    snd = {r['video_id']: r for r in rd(f'{D}/{a}_sounds.csv')}
    for v in vids:
        s = snd.get(v['video_id'])
        if not s: continue
        uses[s['sound_id']].append(dict(a=a, rel=int(v['views']) / med[wk(v['posted_utc'])], t=v['posted_utc'][:10], views=int(v['views']),
                                        title=s['sound_title'], author=s['sound_author'], off=s['official_library_track'] == 'True'))
rows = []
for sid, u in uses.items():
    if len(u) < 3: continue
    m = round(st.median(x['rel'] for x in u), 2); beat = round(sum(x['rel'] > 1 for x in u) / len(u), 2)
    off = sum(x['off'] for x in u) > len(u) / 2
    rows.append(dict(sound_id=sid, title=u[0]['title'], author=u[0]['author'], uses_by_network=len(u), accounts='+'.join(sorted({x['a'] for x in u})),
                     median_relative_views=m, share_beating_week_median=beat, uses_in_october=sum(x['t'].startswith(MONTH) for x in u),
                     last_used=max(x['t'] for x in u), max_views=max(x['views'] for x in u), official_library_track=off,
                     likely_paid_promo=off and len(u) >= 8 and m < 1, proven=m >= 2 and beat >= 0.6,
                     link=f'https://www.tiktok.com/music/x-{sid}'))
rows.sort(key=lambda r: -r['median_relative_views'])
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
print(len(rows), 'sounds;', sum(r['proven'] for r in rows), 'proven;', sum(r['likely_paid_promo'] for r in rows), 'promo ->', OUT)
