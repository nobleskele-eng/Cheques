# Rolling-origin backtest: fit on data up to a cutoff, predict the increment over the next h days.
import json, sys, datetime as dt, statistics as stt
UTC = dt.timezone.utc; DAY = 86400
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

S = sys.argv[1]
def piecewise_last_slope(t, y):
    n = len(t); best = (float('inf'), None)
    for i in range(3, n-3):
        for j in range(i+3, n-3):
            X = [[1, x, max(0, x-t[i]), max(0, x-t[j])] for x in t]
            beta, sse = fit(X, y)
            if beta and sse < best[0]: best = (sse, beta)
    b = best[1]; return b[1] + b[2] + b[3]
def lin_slope(t, y):
    n = len(t); mx = sum(t)/n; my = sum(y)/n
    return sum((a-mx)*(b-my) for a, b in zip(t, y)) / sum((a-mx)**2 for a in t)
LAST_TARGET_END = dt.datetime(2026, 10, 14, tzinfo=UTC).timestamp()  # leave a week for recent videos to accrue
res = {}
for h in ['someplace505', 'elsewhere557']:
    pts = json.load(open(f'{S}/data/{h}.daily.json'))
    for m in ['videos', 'views', 'likes']:
        for horizon in [7, 14, 28]:
            errs = {'piecewise': [], 'trailing14': [], 'linear_all': []}
            cut = dt.datetime(2026, 9, 7, tzinfo=UTC).timestamp()
            while cut + horizon*DAY <= LAST_TARGET_END:
                tr = [p for p in pts if p['ts'] <= cut]
                t = [(p['ts'] - tr[0]['ts'])/DAY for p in tr]; y = [p[m] for p in tr]
                actual = [p for p in pts if p['ts'] <= cut + horizon*DAY][-1][m] - y[-1]
                if len(tr) >= 12 and actual > 0:
                    preds = {'piecewise': piecewise_last_slope(t, y) * horizon,
                             'trailing14': (y[-1] - y[-15]) / 14 * horizon,
                             'linear_all': lin_slope(t, y) * horizon}
                    for k, p in preds.items(): errs[k].append(abs(p - actual) / actual)
                cut += 7*DAY
            res[(h, m, horizon)] = {k: (stt.median(e), max(e), len(e)) for k, e in errs.items() if e}
for (h, m, hz), r in res.items():
    print(f'{h:13s} {m:7s} +{hz:2d}d  ' + '  '.join(f'{k}: median err {v[0]:.0%} (worst {v[1]:.0%}, n={v[2]})' for k, v in r.items()))
