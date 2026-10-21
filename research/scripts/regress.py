import json, sys, math, datetime as dt
UTC = dt.timezone.utc
D = lambda t: dt.datetime.fromtimestamp(t, UTC)
T = 1792610809  # API server time at scrape (2026-10-21 19:26:49 UTC)
DAY = 86400
prof = {'someplace505': dict(followers=214189, created=1768022213),
        'elsewhere557': dict(followers=380134, created=1727641854)}

def ols(x, y):
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    sxx = sum((a-mx)**2 for a in x); sxy = sum((a-mx)*(b-my) for a, b in zip(x, y))
    b = sxy/sxx; return my - b*mx, b

def r2(y, yhat):
    my = sum(y)/len(y); sst = sum((a-my)**2 for a in y)
    return 1 - sum((a-b)**2 for a, b in zip(y, yhat))/sst

def fits(t, y):
    out = {}
    a, b = ols(t, y); out['linear'] = dict(slope_per_day=b, r2=r2(y, [a+b*x for x in t]))
    c, r = ols(t, [math.log(v) for v in y]); out['exponential'] = dict(rate_per_day=r, doubling_days=math.log(2)/r if r > 0 else None, r2=r2(y, [math.exp(c+r*x) for x in t]))
    la, k = ols([math.log(x) for x in t], [math.log(v) for v in y]); out['power'] = dict(exponent=k, r2=r2(y, [math.exp(la)*x**k for x in t]))
    return out

result = {}
for h, p in prof.items():
    v = json.load(open(f'{sys.argv[1]}/{h}.items.json'))
    F = v[0]['createTime']; Ltot = sum(x['likes'] for x in v)
    # daily sample points: end of each UTC day from first-video day to snapshot
    day0 = int(D(F).replace(hour=0, minute=0, second=0).timestamp())
    pts = []
    d = day0 + DAY
    while True:
        cut = min(d, T)
        sel = [x for x in v if x['createTime'] < cut]
        L = sum(x['likes'] for x in sel)
        pts.append(dict(ts=cut, videos=len(sel), views=sum(x['views'] for x in sel), likes=L, followers_model=p['followers']*L/Ltot))
        if cut == T: break
        d += DAY
    scen = {'A_buffer_30d': F - 30*DAY, 'B_no_buffer': F, 'C_measured_account_creation': p['created']}
    res = {'first_video': D(F).isoformat(), 'snapshot': D(T).isoformat(), 'n_points': len(pts), 'scenarios': {}}
    for name, t0 in scen.items():
        age = (T - t0)/DAY
        sc = {'start': D(t0).date().isoformat(), 'age_days': round(age, 1),
              'avg_per_day': {m: pts[-1][m]/age for m in ['videos', 'views', 'likes', 'followers_model']}, 'fits': {}}
        t = [(q['ts'] - t0)/DAY for q in pts]
        for m in ['videos', 'views', 'likes', 'followers_model']:
            idx = [i for i, q in enumerate(pts) if q[m] > 0]
            sc['fits'][m] = fits([t[i] for i in idx], [pts[i][m] for i in idx])
        ms = {}
        for target in [10_000, 50_000, 100_000, 200_000, 300_000]:
            hit = next((q for q in pts if q['followers_model'] >= target), None)
            ms[target] = None if hit is None else dict(date=D(hit['ts']).date().isoformat(), days_from_start=round((hit['ts']-t0)/DAY, 1))
        sc['followers_milestones_model'] = ms
        res['scenarios'][name] = sc
    if h == 'elsewhere557':
        cut = int(dt.datetime(2026, 8, 24, 23, 59, 59, tzinfo=UTC).timestamp())
        q = max((q for q in pts if q['ts'] <= cut + 1), key=lambda q: q['ts'])
        res['tokportal_check_2026_08_24'] = dict(model_followers=round(q['followers_model']), tokportal_followers=106685, visible_videos=q['videos'], tokportal_videos=161)
    json.dump(pts, open(f'{sys.argv[1]}/{h}.daily.json', 'w'))
    result[h] = res
json.dump(result, open(f'{sys.argv[1]}/regression.json', 'w'), indent=1)
for h, res in result.items():
    print('=====', h, 'first video', res['first_video'][:10], 'points', res['n_points'], res.get('tokportal_check_2026_08_24', ''))
    for name, sc in res['scenarios'].items():
        a = sc['avg_per_day']
        print(f"  {name}: start {sc['start']} age {sc['age_days']}d | avg/day videos {a['videos']:.2f} views {a['views']:,.0f} likes {a['likes']:,.0f} followers {a['followers_model']:,.0f}")
        for m, f in sc['fits'].items():
            print(f"     {m:16s} lin slope {f['linear']['slope_per_day']:>12,.1f} R2 {f['linear']['r2']:.3f} | exp r {f['exponential']['rate_per_day']:.4f} dbl {f['exponential']['doubling_days'] or 0:.1f}d R2 {f['exponential']['r2']:.3f} | pow k {f['power']['exponent']:.2f} R2 {f['power']['r2']:.3f}")
        print('     milestones', {k: (v['date'], v['days_from_start']) if v else None for k, v in sc['followers_milestones_model'].items()})
