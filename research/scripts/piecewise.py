import json, sys, datetime as dt
UTC = dt.timezone.utc; D = lambda t: dt.datetime.fromtimestamp(t, UTC); DAY = 86400

def solve(A, b):
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-12: return None
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [x - f*y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]

def fit(X, y):
    k = len(X[0]); A = [[sum(r[i]*r[j] for r in X) for j in range(k)] for i in range(k)]
    b = [sum(r[i]*v for r, v in zip(X, y)) for i in range(k)]
    beta = solve(A, b)
    if beta is None: return None, float('inf')
    sse = sum((v - sum(bi*xi for bi, xi in zip(beta, r)))**2 for r, v in zip(X, y))
    return beta, sse

out = {}
for h in ['someplace505', 'elsewhere557']:
    pts = json.load(open(f'{sys.argv[1]}/{h}.daily.json'))
    t0 = pts[0]['ts']; t = [(p['ts'] - t0)/DAY for p in pts]; n = len(t)
    res = {}
    for m in ['videos', 'views', 'likes']:
        y = [p[m] for p in pts]; my = sum(y)/n; sst = sum((v-my)**2 for v in y)
        best = (float('inf'), None)
        for i in range(3, n-3):
            for j in range(i+3, n-3):
                X = [[1, x, max(0, x - t[i]), max(0, x - t[j])] for x in t]
                beta, sse = fit(X, y)
                if sse < best[0]: best = (sse, (i, j, beta))
        sse, (i, j, beta) = best
        a, b1, b2, b3 = beta
        res[m] = dict(break1=D(pts[i]['ts']).date().isoformat(), break2=D(pts[j]['ts']).date().isoformat(),
                      slope1=b1, slope2=b1+b2, slope3=b1+b2+b3, r2=1 - sse/sst)
        print(f"{h} {m:7s} R2 {res[m]['r2']:.4f} | until {res[m]['break1']}: {b1:,.1f}/day | {res[m]['break1']}..{res[m]['break2']}: {b1+b2:,.1f}/day | after {res[m]['break2']}: {b1+b2+b3:,.1f}/day")
    out[h] = res
json.dump(out, open(f'{sys.argv[1]}/piecewise.json', 'w'), indent=1)
