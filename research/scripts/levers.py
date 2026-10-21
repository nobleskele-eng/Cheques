# Which controllable choices go with higher views? Views are normalised to the same account's same-week median.
import json, sys, statistics as st, datetime as dt
from collections import defaultdict, Counter
UTC = dt.timezone.utc
def wk(t): d = dt.datetime.fromtimestamp(t, UTC).date(); return d - dt.timedelta(days=d.weekday())
def summarize(label, groups, min_n=8):
    print(f'  -- {label}')
    for k, vals in groups:
        if len(vals) >= min_n:
            print(f'     {str(k):28s} n={len(vals):>3}  median relative views {st.median(vals):.2f}x  share beating week median {sum(1 for x in vals if x > 1)/len(vals):.0%}')
for h in ['someplace505', 'elsewhere557']:
    v = json.load(open(f'{sys.argv[1]}/data/{h}.tech.json'))
    v = [x for x in v if x['createTime'] >= dt.datetime(2026, 8, 24, tzinfo=UTC).timestamp()]  # active period only
    byw = defaultdict(list)
    for x in v: byw[wk(x['createTime'])].append(x['views'])
    med = {k: st.median(a) for k, a in byw.items()}
    for x in v: x['rel'] = x['views'] / med[wk(x['createTime'])] if med[wk(x['createTime'])] else 0
    print(f'===== {h} (active period from 2026-08-24, n={len(v)})')
    # posts per day and order within day
    byday = defaultdict(list)
    for x in sorted(v, key=lambda x: x['createTime']): byday[dt.datetime.fromtimestamp(x['createTime'], UTC).date()].append(x)
    ppd = defaultdict(list); order = defaultdict(list)
    for d, xs in byday.items():
        b = '1' if len(xs) == 1 else '2-3' if len(xs) <= 3 else '4-6' if len(xs) <= 6 else '7-10' if len(xs) <= 10 else '11+'
        for i, x in enumerate(xs):
            ppd[b].append(x['rel']); order['1st of day' if i == 0 else '2nd-3rd' if i < 3 else '4th-6th' if i < 6 else '7th+'].append(x['rel'])
    print(f'  posts/day: median {st.median(len(a) for a in byday.values())}, max {max(len(a) for a in byday.values())}, days posted {len(byday)}')
    summarize('posts that day', [(k, ppd[k]) for k in ['1', '2-3', '4-6', '7-10', '11+']])
    summarize('order within the day', [(k, order[k]) for k in ['1st of day', '2nd-3rd', '4th-6th', '7th+']])
    hours = defaultdict(list)
    for x in v:
        hr = dt.datetime.fromtimestamp(x['createTime'], UTC).hour
        hours[f'{hr//4*4:02d}-{hr//4*4+3:02d} UTC'].append(x['rel'])
    summarize('posting time (UTC, 4h blocks)', sorted(hours.items()))
    durs = defaultdict(list)
    for x in v:
        d = x['duration'] or 0
        durs['<=6s' if d <= 6 else '7-8s' if d <= 8 else '9-10s' if d <= 10 else '11-13s' if d <= 13 else '14s+'].append(x['rel'])
    summarize('length', [(k, durs[k]) for k in ['<=6s', '7-8s', '9-10s', '11-13s', '14s+']])
    snd = Counter((x['music_title'] or '').strip() for x in v)
    sg = defaultdict(list)
    for x in v:
        t = (x['music_title'] or '').strip()
        generic = t.lower() in ('original sound', 'son original', 'som original', 'audio originale', 'sonido original', 'suara asli') or t.startswith('original sound -')
        sg['generic "original sound"' if generic else ('reused named sound (5+ uses)' if snd[t] >= 5 else 'named sound, used <5x')].append(x['rel'])
    summarize('sound type', sorted(sg.items()))
    top = [(t, [x['rel'] for x in v if (x['music_title'] or '').strip() == t]) for t, c in snd.most_common(6)]
    summarize('most-used sounds', top, min_n=8)
    up = defaultdict(list)
    for x in v:
        if not x['gears']: up['original file served (no re-encode)'].append(x['rel'])
        else:
            mf = max(q['fps'] or 0 for q in x['gears']); mh = max(q['h'] or 0 for q in x['gears'])
            up[('1080p tier, ' if mh >= 1900 else '<1080p tier, ') + ('~60fps' if mf >= 50 else '~30fps')].append(x['rel'])
    summarize('upload quality', sorted(up.items()), min_n=5)
