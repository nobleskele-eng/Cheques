# usage: python3 -I research/scripts/anime_features.py research/data stayvyxed smokinsasa7 .sadaqatt   (17 Nov analysis: anime/research/levers-2026-11-17.md)
# Within-account feature check: does loudness / quality / duration / hour / gap track views x (views / median of previous 10 posts)?
import csv, sys, statistics as st, datetime as dt, math, re
D = sys.argv[1]
def load(h):
    v = {r['video_id']: r for r in csv.DictReader(open(f'{D}/{h}_videos.csv', encoding='utf-8-sig'))}
    e = {r['video_id']: r for r in csv.DictReader(open(f'{D}/{h}_encoding.csv', encoding='utf-8-sig'))}
    c = {r['video_id']: r['caption'] for r in csv.DictReader(open(f'{D}/{h}_captions.csv', encoding='utf-8-sig'))}
    rows = []
    for k, r in v.items():
        t = dt.datetime.strptime(r['posted_utc'], '%Y-%m-%d %H:%M:%S')
        x = e.get(k, {})
        f = lambda s: float(s) if s not in ('', None) else None
        cap = c.get(k, '')
        rows.append(dict(t=t, views=int(r['views']), dur=f(r['duration_s']), loud=f(x.get('loudness')), vq=f(x.get('tiktok_vq_score')),
                         src=f(x.get('source_quality_score')), hour=(t.hour - 5) % 24,  # Toronto-ish local hour (EST)
                         tags=len(re.findall(r'#\w', cap)), caplen=len(cap)))
    rows.sort(key=lambda r: r['t'])
    for i, r in enumerate(rows):
        prev = [p['views'] for p in rows[max(0, i - 10):i]]
        r['x'] = r['views'] / st.median(prev) if len(prev) >= 5 else None
        r['gap_h'] = (r['t'] - rows[i - 1]['t']).total_seconds() / 3600 if i else None
        r['n24'] = sum(1 for p in rows[:i] if (r['t'] - p['t']).total_seconds() < 86400)
    now = max(r['t'] for r in rows)
    return [r for r in rows if r['x'] is not None and (now - r['t']).days >= 2]
def rank(a):
    s = sorted(range(len(a)), key=lambda i: a[i]); r = [0] * len(a)
    for j, i in enumerate(s): r[i] = j
    return r
def spear(a, b):
    ra, rb = rank(a), rank(b); n = len(a)
    ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else float('nan')
feats = ['loud', 'vq', 'src', 'dur', 'hour', 'gap_h', 'n24', 'tags', 'caplen']
for h in sys.argv[2:]:
    rows = load(h)
    out = []
    for f in feats:
        pr = [(r[f], r['x']) for r in rows if r[f] is not None]
        if len(pr) >= 15:
            out.append(f"{f} {spear([p[0] for p in pr], [p[1] for p in pr]):+.2f} (n={len(pr)})")
    print(h, '|', '; '.join(out))
    # top-quartile vs bottom-quartile medians for loudness and gap
    xs = sorted(r['x'] for r in rows); q1, q3 = xs[len(xs)//4], xs[3*len(xs)//4]
    for f in ['loud', 'vq', 'dur', 'gap_h', 'hour']:
        top = [r[f] for r in rows if r['x'] >= q3 and r[f] is not None]; bot = [r[f] for r in rows if r['x'] <= q1 and r[f] is not None]
        if top and bot: print(f'   {f}: top-quartile median {st.median(top):.1f} vs bottom {st.median(bot):.1f}')
