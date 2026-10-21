import json, sys, statistics as st, datetime as dt
from collections import Counter
S, h = sys.argv[1], sys.argv[2]; UTC = dt.timezone.utc
items = json.load(open(f'{S}/data/{h}.items.json'))
tech = {x['id']: x for x in json.load(open(f'{S}/data/{h}.tech.json'))}
mj = json.load(open(f'{S}/data/{h}.music.json'))
nick = mj['nickname']; mus = {x['id']: x for x in mj['items']}
D = lambda t: dt.datetime.fromtimestamp(t, UTC)
print(f"{'posted (UTC)':16s} {'views':>6} {'like%':>6} {'shr%':>5} {'save%':>5} {'cmt':>3} {'len':>3} {'res/fps':>12} {'orig':>4}  sound (origin | title | age d)")
rows = []
for x in items:
    t, m = tech[x['id']], mus[x['id']]
    v = max(1, x['views'])
    g = max(t['gears'], key=lambda q: ((q['h'] or 0), q['bitrate'] or 0)) if t['gears'] else None
    own = m['music_author'] == nick
    mt = int(m['music_id']) >> 32; age = (x['createTime'] - mt) / 86400
    origin = 'OWN-NEW' if own and abs(x['createTime'] - mt) < 3600 else ('own-reuse' if own else ('other-acct' if m['original'] else 'LIBRARY'))
    resfps = f"{g['h']}p/{g['fps']}" if g else 'original'
    print(f"{D(x['createTime']):%Y-%m-%d %H:%M} {x['views']:>6,} {x['likes']/v:>6.1%} {x['shares']/v:>5.1%} {x['saves']/v:>5.1%} {x['comments']:>3} {x['duration']:>3} {resfps:>12} {str(not t['gears'])[:1]:>4}  {origin:10s} | {(m['music_title'] or '')[:24]:24s} | {age:>5.0f}")
    rows.append(dict(x, origin=origin, age=age, matched=m['matched_song'], resfps=resfps, orig=not t['gears']))
v = [x['views'] for x in items]
lr = [x['likes'] / max(1, x['views']) for x in items]; sr = [x['shares'] / max(1, x['views']) for x in items]; sv = [x['saves'] / max(1, x['views']) for x in items]
print(f"\nvideos {len(items)} | views median {st.median(v):,.0f} min {min(v):,} max {max(v):,} | like rate median {st.median(lr):.1%} (max {max(lr):.1%}) | share {st.median(sr):.2%} | save {st.median(sv):.2%} | comments total {sum(x['comments'] for x in items)}")
print('sound origins', Counter(r['origin'] for r in rows), '| matched commercial song', sum(1 for r in rows if r['matched']))
print('durations', Counter(x['duration'] for x in items).most_common(6))
days = Counter(D(x['createTime']).date() for x in items); print('days posted', len(days), 'posts/day median', st.median(days.values()), 'span', min(days), '->', max(days))
print('captions non-empty:', sum(1 for x in items if x['desc'].strip()), '| examples:', [x['desc'][:50] for x in items if x['desc'].strip()][:6])
print('res/fps', Counter(r['resfps'] for r in rows).most_common(5))
json.dump(rows, open(f'{S}/data/{h}.combined.json', 'w'))
