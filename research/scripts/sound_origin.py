# Classify each video's sound by when and by whom it was created, then compare same-week relative views.
import json, sys, statistics as st, datetime as dt
from collections import defaultdict, Counter
UTC = dt.timezone.utc
S = sys.argv[1]
def wk(t): d = dt.datetime.fromtimestamp(t, UTC).date(); return d - dt.timedelta(days=d.weekday())
data = {h: json.load(open(f'{S}/data/{h}.music.json')) for h in ['someplace505', 'elsewhere557']}
nick = {h: data[h]['nickname'] for h in data}
allmusic = defaultdict(set)
for h in data:
    for x in data[h]['items']: allmusic[x['music_id']].add(h)
for h in data:
    v = data[h]['items']
    deltas = []
    for x in v:
        mt = int(x['music_id']) >> 32
        x['delta_s'] = x['createTime'] - mt
        x['own'] = x['music_author'] == nick[h]
        if x['own'] and abs(x['delta_s']) <= 3600: x['cat'] = 'A: new sound created by this upload'
        elif x['own']: x['cat'] = 'B: re-used its own earlier sound'
        elif x['original']: x['cat'] = "C: picked another account's sound"
        else: x['cat'] = 'D: picked an official library track'
        deltas.append(x['delta_s'])
    print(f'===== {h} (nickname {nick[h]!r})')
    own = [x['delta_s'] for x in v if x['own']]
    print('  seconds between sound creation and video post, own sounds: ', sorted(own)[:5], '...', 'median', st.median(own) if own else '-')
    print('  sound categories:', dict(Counter(x['cat'] for x in v)))
    other = Counter(x['music_author'] for x in v if not x['own'])
    print('  distinct other authors:', len(other), '| blank-name authors (invisible chars):', sum(n for a, n in other.items() if a and all(ch in '￴‍ ㅤ⠀' for ch in a)), 'videos')
    print('  top other authors:', [(repr(a)[:30], n) for a, n in other.most_common(5)])
    print('  matched to a commercial song:', sum(1 for x in v if x['matched_song']), '/', len(v), '| commerce flag:', sum(1 for x in v if x['commerce']), '| shared sound ids with sibling:', sum(1 for x in v if len(allmusic[x['music_id']]) > 1))
    print('  sound age when used (days, non-own):', 'median', round(st.median([x['delta_s']/86400 for x in v if not x['own']]), 1))
    act = [x for x in v if x['createTime'] >= dt.datetime(2026, 8, 24, tzinfo=UTC).timestamp()]
    byw = defaultdict(list)
    for x in act: byw[wk(x['createTime'])].append(x['views'])
    med = {k: st.median(a) for k, a in byw.items()}
    groups = defaultdict(list)
    for x in act: groups[x['cat']].append(x['views'] / med[wk(x['createTime'])])
    for k in sorted(groups):
        a = groups[k]; print(f'   {k:42s} n={len(a):>3}  median rel views {st.median(a):.2f}x  beat week median {sum(1 for y in a if y > 1)/len(a):.0%}')
    g2 = defaultdict(list)
    for x in act: g2['matched commercial song' if x['matched_song'] else 'no song match'].append(x['views'] / med[wk(x['createTime'])])
    for k in sorted(g2):
        a = g2[k]; print(f'   {k:42s} n={len(a):>3}  median rel views {st.median(a):.2f}x  beat week median {sum(1 for y in a if y > 1)/len(a):.0%}')
json.dump(data, open(f'{S}/data/music_classified.json', 'w'))
