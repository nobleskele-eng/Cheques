import json, sys, math, datetime as dt, statistics as stt
UTC = dt.timezone.utc; DAY = 86400
D = lambda t: dt.datetime.fromtimestamp(t, UTC)
S = sys.argv[1]
print('== 1. view-count precision')
for h in ['someplace505', 'elsewhere557']:
    v = json.load(open(f'{S}/data/{h}.items.json'))
    big = [x['views'] for x in v if x['views'] >= 1_000_000]
    rounded = [x for x in big if x % 100_000 == 0]
    mid = [x['views'] for x in v if 10_000 <= x['views'] < 1_000_000]
    rmid = [x for x in mid if x % 100 == 0]
    tot = sum(x['views'] for x in v)
    maxerr = sum(50_000 for _ in rounded) + sum(50 for _ in rmid)
    print(f'  {h}: {len(rounded)}/{len(big)} videos >=1M are multiples of 100K; {len(rmid)}/{len(mid)} 10K-1M are multiples of 100; worst-case rounding error on total views ±{maxerr:,} = ±{maxerr/tot:.2%}')
    likes_round = sum(1 for x in v if x['likes'] >= 1_000_000 and x['likes'] % 100_000 == 0)
    print(f'     likes >=1M rounded: {likes_round}/{sum(1 for x in v if x["likes"]>=1_000_000)}')

print('== 2. growth similarity (aligned at views takeoff)')
pw = json.load(open(f'{S}/data/piecewise.json'))
daily = {h: json.load(open(f'{S}/data/{h}.daily.json')) for h in ['someplace505', 'elsewhere557']}
take = {h: dt.datetime.fromisoformat(pw[h]['views']['break1']).replace(tzinfo=UTC).timestamp() for h in daily}
def at(h, t, m='views'):
    pts = [p for p in daily[h] if p['ts'] <= t]
    return pts[-1][m] if pts else 0
inc = {}
for h in daily:
    base = at(h, take[h]); tot = daily[h][-1]['views']
    row = []
    for k in [7, 14, 21, 28, 35, 42, 49]:
        row.append((k, at(h, take[h] + k*DAY) - base))
    inc[h] = [at(h, take[h] + (k+1)*DAY) - at(h, take[h] + k*DAY) for k in range(50)]
    print(f'  {h}: takeoff {D(take[h]).date()} | views before takeoff {base/1e6:.1f}M | views gained after k days: ' + ', '.join(f'{k}d {g/1e6:.0f}M' for k, g in row))
    vids = json.load(open(f'{S}/data/{h}.items.json'))
    pre = [x for x in vids if x['createTime'] < take[h]]
    print(f'     pre-takeoff videos: {len(pre)}, their median views {stt.median([x["views"] for x in pre]) if pre else 0:,.0f}')
a, b = inc['someplace505'], inc['elsewhere557']
ma, mb = sum(a)/len(a), sum(b)/len(b)
r = sum((x-ma)*(y-mb) for x, y in zip(a, b)) / math.sqrt(sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b))
print(f'  Pearson r of daily new views, aligned at takeoff, days 0-49: {r:.2f}')
wa = [sum(a[i:i+7]) for i in range(0, 49, 7)]; wb = [sum(b[i:i+7]) for i in range(0, 49, 7)]
ma, mb = sum(wa)/7, sum(wb)/7
rw = sum((x-ma)*(y-mb) for x, y in zip(wa, wb)) / math.sqrt(sum((x-ma)**2 for x in wa) * sum((y-mb)**2 for y in wb))
print(f'  Pearson r of weekly new views aligned (7 weeks): {rw:.2f}; weekly M: someplace {[round(x/1e6,1) for x in wa]} elsewhere {[round(x/1e6,1) for x in wb]}')
for h in daily:
    v = json.load(open(f'{S}/data/{h}.items.json'))
    hits = sum(1 for x in v if x['views'] >= 1_000_000)
    print(f'  {h}: 1M+ hit rate {hits}/{len(v)} = {hits/len(v):.1%}; 100K+ {sum(1 for x in v if x["views"]>=100_000)/len(v):.1%}; <10K {sum(1 for x in v if x["views"]<10_000)/len(v):.1%}')
