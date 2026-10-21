#!/usr/bin/env python3
"""Per-video success model for @someplace505 and @elsewhere557.

Run from the repo root:   python3 research/model/success_model.py
Needs:                    numpy
Reads:                    research/data/{account}_videos.csv, _encoding.csv, _sounds.csv
                          research/data/extra_features.csv (optional, keyed by video_id)
Writes:                   research/success-model.md, research/model/results.json

What it estimates: the odds that a single video does well, given choices the
creator controls, using these two (already successful) accounts. It does NOT
estimate the odds that a new account succeeds - there are no failed accounts
in the data. Account-level numbers in the report are labelled as upper bounds.
"""
import csv
import datetime as dt
import json
import math
import os
from collections import defaultdict

import numpy as np

RESEARCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RESEARCH, 'data')
ACCOUNTS = ['someplace505', 'elsewhere557']
UTC = dt.timezone.utc
# Takeoff dates from the piecewise fit in tiktok-growth-regression.md. Videos before
# these dates are the "cold start" reference; videos after them train the model.
TAKEOFF = {'someplace505': dt.datetime(2026, 8, 31, tzinfo=UTC),
           'elsewhere557': dt.datetime(2026, 8, 8, tzinfo=UTC)}
ACCRUAL_DAYS = 7          # drop the newest week: those videos are still collecting views
SPLIT = dt.datetime(2026, 10, 1, tzinfo=UTC)   # validation: train before, test after
LAMBDA = 1.0              # L2 penalty (keeps correlated features stable)
N_BOOT = 300
MIN_LABELLED = 30         # extra-research columns need at least this many labelled videos
SEED = 7
TARGETS = [('beat_median', "beats the account's median for that week"),
           ('hit_100k', 'reaches 100K+ views'),
           ('hit_1m', 'reaches 1M+ views')]


def read(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def parse_time(s):
    return dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').replace(tzinfo=UTC)


def monday(t):
    d = t.date()
    return d - dt.timedelta(days=d.weekday())


def load_rows():
    rows = []
    for acct in ACCOUNTS:
        enc = {r['video_id']: r for r in read(f'{DATA}/{acct}_encoding.csv')}
        snd = {r['video_id']: r for r in read(f'{DATA}/{acct}_sounds.csv')}
        for v in read(f'{DATA}/{acct}_videos.csv'):
            e, s = enc.get(v['video_id']), snd.get(v['video_id'])
            if not e or not s:
                continue
            rows.append(dict(id=v['video_id'], acct=acct, t=parse_time(v['posted_utc']), views=int(v['views']),
                             duration=float(v['duration_s'] or 0), enc=e, snd=s))
    rows.sort(key=lambda r: r['t'])
    return rows


def derive(rows):
    week = defaultdict(list)
    for r in rows:
        week[(r['acct'], monday(r['t']))].append(r['views'])
    wmed = {k: float(np.median(v)) for k, v in week.items()}
    day = defaultdict(list)
    for r in rows:
        day[(r['acct'], r['t'].date())].append(r)
    for posts in day.values():
        for i, r in enumerate(sorted(posts, key=lambda r: r['t'])):
            r['posts_that_day'] = len(posts)
            r['first_of_day'] = 1.0 if i == 0 else 0.0
    by_sound = defaultdict(list)
    for r in rows:
        e, s = r['enc'], r['snd']
        r['beat_median'] = 1.0 if r['views'] > wmed[(r['acct'], monday(r['t']))] else 0.0
        r['hit_100k'] = 1.0 if r['views'] >= 100_000 else 0.0
        r['hit_1m'] = 1.0 if r['views'] >= 1_000_000 else 0.0
        origin = s['sound_origin']
        r['snd_own'] = 1.0 if origin in ('new sound created by this upload', 're-used its own earlier sound') else 0.0
        r['snd_other'] = 1.0 if origin == "picked another account's sound" else 0.0
        r['matched_song'] = 1.0 if s['matched_commercial_song'] == 'True' else 0.0
        r['orig_file'] = 1.0 if e['original_file_served'] == 'True' else 0.0
        res = [int(x) for x in e['best_tier_res'].split('x')] if e['best_tier_res'] else []
        r['has_1080'] = 1.0 if r['orig_file'] or (res and max(res) >= 1900) else 0.0
        r['fps_60'] = (1.0 if float(e['best_tier_fps']) >= 50 else 0.0) if e['best_tier_fps'] else float('nan')
        r['log_sound_age'] = math.log1p(max(0.0, float(s['sound_age_days_at_post'])))
        r['acct_someplace'] = 1.0 if r['acct'] == 'someplace505' else 0.0
        prior = by_sound[s['sound_id']]
        r['log_prior_uses'] = math.log1p(len(prior))
        r['prior_beat_rate'] = sum(p['beat_median'] for p in prior) / len(prior) if prior else 0.5
        prior.append(r)
    return rows


BASE_FEATURES = [
    ('acct_someplace', 'binary', 'Account is @someplace505 (control, not a choice)'),
    ('snd_other', 'binary', "Sound: picked another account's sound (vs official library track)"),
    ('snd_own', 'binary', 'Sound: own audio uploaded with the video (vs official library track)'),
    ('matched_song', 'binary', 'TikTok matched the audio to a commercial song'),
    ('orig_file', 'binary', 'Served as the original file (third-party upload method)'),
    ('has_1080', 'binary', 'Has a 1080p (or higher) version'),
    ('fps_60', 'binary', 'Uploaded at ~60 fps'),
    ('duration', 'cont', 'Length (seconds)'),
    ('posts_that_day', 'cont', 'Posts by the account that day'),
    ('first_of_day', 'binary', "First post of the account's day"),
    ('log_sound_age', 'cont', 'Sound age when used (log days)'),
    ('log_prior_uses', 'cont', 'Earlier uses of the same sound by these accounts (log count)'),
    ('prior_beat_rate', 'cont', 'Share of those earlier uses that beat their week median'),
]


def add_extra_features(rows, features):
    path = f'{DATA}/extra_features.csv'
    skipped = []
    if not os.path.exists(path):
        return features, [], skipped
    extra = {r['video_id']: r for r in read(path)}
    cols = [c for c in (read(path)[0].keys() if extra else []) if c != 'video_id']
    added = []
    for col in cols:
        vals = [extra.get(r['id'], {}).get(col, '') for r in rows]
        present = [v for v in vals if v.strip() != '']
        if len(present) < MIN_LABELLED:
            skipped.append(f'{col} ({len(present)} labelled)')
            continue
        try:
            nums = [float(v) for v in present]
            name = f'x_{col}'
            for r, v in zip(rows, vals):
                r[name] = float(v) if v.strip() != '' else float('nan')
            binary = set(nums) <= {0.0, 1.0}
            features.append((name, 'binary' if binary else 'cont', f'[your research] {col}'))
            added.append(name)
        except ValueError:
            counts = defaultdict(int)
            for v in present:
                counts[v] += 1
            keep = [c for c, n in sorted(counts.items(), key=lambda kv: -kv[1]) if n >= 10][1:]  # most common = baseline
            for cat in keep:
                name = f'x_{col}={cat}'
                for r, v in zip(rows, vals):
                    r[name] = 1.0 if v == cat else (0.0 if v.strip() != '' else float('nan'))
                features.append((name, 'binary', f'[your research] {col} = {cat}'))
                added.append(name)
    return features, added, skipped


def matrix(rows, features, stats=None):
    X = np.array([[r.get(f, float('nan')) for f, _, _ in features] for r in rows], dtype=float)
    if stats is None:
        with np.errstate(all='ignore'):
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', RuntimeWarning)
                mean = np.nanmean(X, axis=0)
                std = np.nanstd(X, axis=0)
        mean = np.where(np.isnan(mean), 0.0, mean)
        std = np.where(np.isnan(std) | (std == 0), 1.0, std)
        stats = (mean, std)
    mean, std = stats
    X = np.where(np.isnan(X), mean, X)
    for j, (_, kind, _) in enumerate(features):
        if kind == 'cont':
            X[:, j] = (X[:, j] - mean[j]) / std[j]
    return X, stats


def fit(X, y, lam=LAMBDA):
    Xb = np.hstack([np.ones((len(X), 1)), X])
    w = np.zeros(Xb.shape[1])
    R = lam * np.eye(Xb.shape[1])
    R[0, 0] = 0.0
    for _ in range(100):
        p = 1 / (1 + np.exp(-(Xb @ w)))
        step = np.linalg.solve((Xb * (p * (1 - p))[:, None]).T @ Xb + R, Xb.T @ (p - y) + R @ w)
        w -= step
        if np.max(np.abs(step)) < 1e-9:
            break
    return w


def predict(w, X):
    return 1 / (1 + np.exp(-(np.hstack([np.ones((len(X), 1)), X]) @ w)))


def recalibrate(w, X_recent, target_rate):
    """Shift the intercept so the average prediction on the most recent period matches its observed rate."""
    z = np.hstack([np.ones((len(X_recent), 1)), X_recent]) @ w
    lo, hi = -10.0, 10.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if np.mean(1 / (1 + np.exp(-(z + mid)))) > target_rate:
            hi = mid
        else:
            lo = mid
    w2 = w.copy()
    w2[0] += (lo + hi) / 2
    return w2


def auc(y, p):
    order = np.argsort(p)
    ranks = np.empty(len(p))
    ranks[order] = np.arange(1, len(p) + 1)
    pos = y == 1
    n1, n0 = pos.sum(), (~pos).sum()
    if n1 == 0 or n0 == 0:
        return float('nan')
    return (ranks[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def scenario_rows(train_rows):
    med_age = float(np.median([r['log_sound_age'] for r in train_rows]))
    mean_match = float(np.mean([r['matched_song'] for r in train_rows]))
    base = dict(snd_other=0.0, snd_own=0.0, matched_song=mean_match, orig_file=0.0, has_1080=1.0, fps_60=0.0,
                log_sound_age=med_age, log_prior_uses=0.0, prior_beat_rate=0.5)
    s = [
        ('Plan A', "Another account's sound (new to these accounts), 1080p, 30 fps, 11 s, 3 posts/day",
         dict(base, snd_other=1.0, duration=11, posts_that_day=3, first_of_day=1 / 3)),
        ('Plan A at 60 fps', 'Same as Plan A but uploaded at 60 fps',
         dict(base, snd_other=1.0, fps_60=1.0, duration=11, posts_that_day=3, first_of_day=1 / 3)),
        ('Same, reusing a proven sound', 'Plan A, but the sound was used twice before here and both times beat the median',
         dict(base, snd_other=1.0, duration=11, posts_that_day=3, first_of_day=1 / 3,
              log_prior_uses=math.log1p(2), prior_beat_rate=1.0)),
        ("@elsewhere557's typical", "Another account's sound, 1080p, 60 fps, 8 s, 8 posts/day",
         dict(base, snd_other=1.0, fps_60=1.0, duration=8, posts_that_day=8, first_of_day=1 / 8)),
        ('Official library track', 'Official library track, 1080p, 60 fps, 8 s, 8 posts/day',
         dict(base, fps_60=1.0, duration=8, posts_that_day=8, first_of_day=1 / 8)),
        ('@someplace505 hit recipe', 'Own audio + original-file upload (third-party tool), 9 s, 3 posts/day',
         dict(base, snd_own=1.0, orig_file=1.0, log_sound_age=0.0, duration=9, posts_that_day=3, first_of_day=1 / 3)),
    ]
    out = []
    for name, desc, feats in s:
        for acct, flag in (('someplace505', 1.0), ('elsewhere557', 0.0)):
            out.append(dict(name=name, desc=desc, baseline=acct, row=dict(feats, acct_someplace=flag)))
    return out


def main():
    rows = derive(load_rows())
    snapshot = max(r['t'] for r in rows)
    cutoff = snapshot - dt.timedelta(days=ACCRUAL_DAYS)
    features = list(BASE_FEATURES)
    features, extra_added, extra_skipped = add_extra_features(rows, features)
    active = [r for r in rows if TAKEOFF[r['acct']] <= r['t'] <= cutoff]
    cold = [r for r in rows if r['t'] < TAKEOFF[r['acct']]]
    train = [r for r in active if r['t'] < SPLIT]
    test = [r for r in active if r['t'] >= SPLIT]
    rng = np.random.default_rng(SEED)
    results = dict(snapshot=snapshot.isoformat(), n_active=len(active), n_train=len(train), n_test=len(test),
                   extra_features=extra_added, extra_skipped=extra_skipped, targets={})
    Xtr, st_tr = matrix(train, features)
    Xte, _ = matrix(test, features, st_tr)
    Xall, st_all = matrix(active, features)
    scen = scenario_rows(active)
    Xsc, _ = matrix([s['row'] for s in scen], features, st_all)
    recent_mask = np.array([r['t'] >= SPLIT for r in active])
    for tgt, label in TARGETS:
        ytr = np.array([r[tgt] for r in train])
        yte = np.array([r[tgt] for r in test])
        yall = np.array([r[tgt] for r in active])
        w = fit(Xtr, ytr)
        pte = predict(w, Xte)
        brier = float(np.mean((pte - yte) ** 2))
        brier_base = float(np.mean((ytr.mean() - yte) ** 2))
        wall = fit(Xall, yall)
        absolute = tgt != 'beat_median'
        recent_rate = float(yall[recent_mask].mean())
        wcal = recalibrate(wall, Xall[recent_mask], recent_rate) if absolute else wall
        boot_w, boot_sc = [], []
        for _ in range(N_BOOT):
            idx = rng.integers(0, len(active), len(active))
            if yall[idx].min() == yall[idx].max():
                continue
            wb = fit(Xall[idx], yall[idx])
            boot_w.append(wb)
            boot_sc.append(predict(recalibrate(wb, Xall[recent_mask], recent_rate) if absolute else wb, Xsc))
        boot_w, boot_sc = np.array(boot_w), np.array(boot_sc)
        effects = []
        for j, (f, kind, desc) in enumerate(features):
            scale = st_all[1][j] if kind == 'cont' else 1.0
            unit = f'per +{scale:.2g}' if kind == 'cont' else 'yes vs no'
            b = boot_w[:, j + 1]
            effects.append(dict(feature=f, desc=desc, unit=unit, odds_ratio=float(np.exp(wall[j + 1])),
                                lo=float(np.exp(np.percentile(b, 2.5))), hi=float(np.exp(np.percentile(b, 97.5)))))
        psc = predict(wcal, Xsc)
        scen_out = [dict(name=s['name'], desc=s['desc'], baseline=s['baseline'], p=float(psc[i]),
                         lo=float(np.percentile(boot_sc[:, i], 5)), hi=float(np.percentile(boot_sc[:, i], 95)))
                    for i, s in enumerate(scen)]
        results['targets'][tgt] = dict(label=label, base_rate_train=float(ytr.mean()), base_rate_test=float(yte.mean()),
                                       auc_test=float(auc(yte, pte)), brier_test=brier, brier_base=brier_base,
                                       skill=1 - brier / brier_base if brier_base else float('nan'),
                                       mean_pred_test=float(pte.mean()), effects=effects, scenarios=scen_out,
                                       base_rate_all=float(yall.mean()), recent_rate=recent_rate,
                                       calibrated_to_recent=absolute)
    cold_out = {}
    for acct in ACCOUNTS:
        c = [r for r in cold if r['acct'] == acct]
        a = [r for r in active if r['acct'] == acct]
        cold_out[acct] = dict(n_cold=len(c), cold_median=float(np.median([r['views'] for r in c])) if c else None,
                              cold_100k=sum(r['hit_100k'] for r in c), cold_1m=sum(r['hit_1m'] for r in c),
                              n_active=len(a), active_median=float(np.median([r['views'] for r in a])),
                              active_1m_rate=float(np.mean([r['hit_1m'] for r in a])))
    results['cold_start'] = cold_out
    plan = {}
    for t in ('hit_100k', 'hit_1m'):
        for s in results['targets'][t]['scenarios']:
            if s['name'] == 'Plan A':
                n = 90
                plan[(t, s['baseline'])] = dict(n_posts=n, expected=s['p'] * n, exp_lo=s['lo'] * n, exp_hi=s['hi'] * n)
    results['plan_90_posts'] = {f'{k[0]}|{k[1]}': v for k, v in plan.items()}
    with open(os.path.join(RESEARCH, 'model', 'results.json'), 'w') as f:
        json.dump(results, f, indent=1)
    write_report(results, features)
    print(json.dumps({t: dict(auc=round(v['auc_test'], 3), skill=round(v['skill'], 3)) for t, v in results['targets'].items()}))


def pct(x):
    return f'{100 * x:.0f}%' if x >= 0.095 or x == 0 else f'{100 * x:.1f}%'


def write_report(res, features):
    T = res['targets']
    L = []
    a = L.append
    a('# Success Model: Per-Video Odds\n')
    a(f"*Generated by `research/model/success_model.py`. Data snapshot: {res['snapshot'][:16].replace('T', ' ')} UTC. "
      'Re-run the script after adding data; this file is overwritten.*\n')
    a('> **What this can tell you:** the odds that a single video does well, given choices you control. It\'s estimated from '
      f"{res['n_active']} videos posted after each account's takeoff.\n>\n"
      '> **What it can\'t tell you:** the odds that a *new account* succeeds. Both accounts in the data succeeded, and there are '
      'no failed accounts to compare against. Every account-level number below assumes your videos perform like these established '
      'accounts\' videos, so treat it as an **upper bound**. The data contains **no reliable cold-start discount**.\n')
    if res['extra_features']:
        a(f"**Your research features included:** {', '.join('`' + x + '`' for x in res['extra_features'])}\n")
    else:
        a('**Your research features included:** none yet. Add `research/data/extra_features.csv` (see `research/model/README.md`).\n')
    if res.get('extra_skipped'):
        a(f"**Skipped (fewer than {MIN_LABELLED} labelled videos):** {', '.join(res['extra_skipped'])}\n")

    a('## 0. Bottom line (auto-generated from the numbers below)\n')
    weak = [T[t]['label'] for t, _ in TARGETS if not T[t]['auc_test'] >= 0.6]
    ok = [f"{T[t]['label']} (AUC {T[t]['auc_test']:.2f})" for t, _ in TARGETS if T[t]['auc_test'] >= 0.6]
    a(f"1. **Where the model has some predictive power:** {'; '.join(ok) if ok else 'none'}.")
    if weak:
        a(f"2. **Where it can't predict:** {'; '.join(weak)}. On held-out October videos it did no better than a coin flip, so treat those numbers as base rates, not forecasts.")
    else:
        a('2. **Every target is predicted better than chance** on held-out October videos.')
    sig = []
    for j, (f, kind, desc) in enumerate(features):
        if f == 'acct_someplace':
            continue
        dirs = []
        short = {'beat_median': 'beating the week median', 'hit_100k': '100K+', 'hit_1m': '1M+'}
        for t, _ in TARGETS:
            e = T[t]['effects'][j]
            if e['lo'] > 1:
                dirs.append(f"helps {short[t]} ({e['odds_ratio']:.1f}x odds)")
            elif e['hi'] < 1:
                dirs.append(f"hurts {short[t]} ({e['odds_ratio']:.2f}x odds)")
        if dirs:
            sig.append(f"   - {desc}: {', '.join(dirs)}")
    a('3. **Choices with a consistent effect** (the 95% bootstrap range stays on one side of "no effect"):')
    L.extend(sig if sig else ['   - none'])
    r1m, r100k = T['hit_1m']['recent_rate'], T['hit_100k']['recent_rate']
    a(f"4. **Absolute odds are anchored to the most recent period (Oct 1–14):** {pct(r100k)} of videos reached 100K+ and {pct(r1m)} reached 1M+. "
      f"Over the whole post-takeoff period those rates were {pct(T['hit_100k']['base_rate_all'])} and {pct(T['hit_1m']['base_rate_all'])}; both accounts are cooling.")
    a('5. **No account-level success probability is given.** The data has no failed accounts (see §3).\n')

    a('## 1. Does the model predict anything? (trained on Aug–Sep, tested on Oct 1–14)\n')
    a('| Success means… | Base rate (test) | Model\'s average prediction | Ranking accuracy (AUC) | Improvement over guessing the base rate |')
    a('|---|---|---|---|---|')
    for t, _ in TARGETS:
        v = T[t]
        a(f"| {v['label']} | {pct(v['base_rate_test'])} | {pct(v['mean_pred_test'])} | {v['auc_test']:.2f} | {100 * v['skill']:+.0f}% |")
    a(f"\n- **Sample:** {res['n_train']} training videos, {res['n_test']} test videos.")
    a('- **AUC:** 0.50 is a coin flip, 1.00 is perfect. Around 0.6–0.7 is weak-to-moderate.')
    a('- **Improvement over guessing:** how much better the model\'s probabilities are than always guessing the base rate (Brier skill). Negative means worse than guessing.\n')

    a('## 2. Scenarios: chance that one video succeeds\n')
    a('- **Cells:** the model\'s probability, with a 90% bootstrap range in brackets.')
    a('- **Two baselines:** as if the video were posted on an account like @someplace505, or like @elsewhere557.')
    a('- **Anchoring:** 100K+ and 1M+ are anchored to October rates. "Beats week median" is relative, so it isn\'t anchored.')
    if T['hit_1m']['auc_test'] < 0.6:
        a(f"- **⚠ The 1M+ column isn't validated** (held-out AUC {T['hit_1m']['auc_test']:.2f}): differences between plans there are not reliable.")
    a('')
    names = []
    for s in T['hit_1m']['scenarios']:
        if s['name'] not in names:
            names.append(s['name'])
    for base in ACCOUNTS:
        a(f'**Baseline: an account like @{base}**\n')
        a('| Plan | Beats week median | 100K+ views | 1M+ views |')
        a('|---|---|---|---|')
        for n in names:
            cells = []
            for t, _ in TARGETS:
                s = next(x for x in T[t]['scenarios'] if x['name'] == n and x['baseline'] == base)
                cells.append(f"{pct(s['p'])} ({pct(s['lo'])}–{pct(s['hi'])})")
            desc = next(x['desc'] for x in T['hit_1m']['scenarios'] if x['name'] == n)
            a(f'| **{n}**: {desc} | ' + ' | '.join(cells) + ' |')
        a('')

    a('## 3. Account level: why there\'s no "chance your account succeeds"\n')
    a('Turning per-video odds into an account-level probability would assume a new account\'s videos perform like these established accounts\' videos, which already reach 200K–380K followers and a sibling network.')
    a('At those rates, almost any plan "guarantees" a hit within 90 posts, which says nothing about a new account.')
    a('So here are only the **expected counts on an account like these, at October rates**. That\'s an upper bound for you, not a forecast.\n')
    a('| Baseline | Plan A, 90 posts (3/day for 30 days): expected 100K+ videos | Expected 1M+ videos |')
    a('|---|---|---|')
    P = res['plan_90_posts']
    for base in ACCOUNTS:
        h, m = P[f'hit_100k|{base}'], P[f'hit_1m|{base}']
        a(f"| @{base} | {h['expected']:.0f} ({h['exp_lo']:.0f}–{h['exp_hi']:.0f}) | {m['expected']:.1f} ({m['exp_lo']:.1f}–{m['exp_hi']:.1f}) |")
    a('\n**The only cold-start evidence** is each account\'s videos posted before its takeoff:\n')
    a('| Account | Videos before takeoff | Their median views | 100K+ | 1M+ | After takeoff: median views / 1M+ rate |')
    a('|---|---|---|---|---|---|')
    for acct, c in res['cold_start'].items():
        a(f"| @{acct} | {c['n_cold']} | {c['cold_median']:,.0f} | {c['cold_100k']:.0f} | {c['cold_1m']:.0f} | "
          f"{c['active_median']:,.0f} / {pct(c['active_1m_rate'])} |")
    a('\nTwo accounts, with very different starts, can\'t produce a cold-start rate. @someplace505\'s first videos barely moved; @elsewhere557\'s did well from the start.')
    a('**The way to get a real account-level estimate is your own data:**')
    a('1. Log your first 60–120 posts with the same columns.')
    a('2. Add them to `research/data/`.')
    a('3. Re-run this model.\n')

    a('## 4. Which choices matter (odds ratios, all post-takeoff videos)\n')
    a('- **Reading an odds ratio:** above 1 helps, below 1 hurts. **Bold** means the 95% bootstrap range excludes 1, i.e. a consistent direction.')
    a('- **Continuous features** are scaled per one standard deviation; the step size is shown in the "Unit" column.\n')
    a('| Feature | Unit | Beats week median | 100K+ | 1M+ |')
    a('|---|---|---|---|---|')
    for j, (f, kind, desc) in enumerate(features):
        cells = []
        for t, _ in TARGETS:
            e = T[t]['effects'][j]
            txt = f"{e['odds_ratio']:.2f} ({e['lo']:.2f}–{e['hi']:.2f})"
            cells.append(f'**{txt}**' if e['lo'] > 1 or e['hi'] < 1 else txt)
        a(f"| {desc} | {T['hit_1m']['effects'][j]['unit']} | " + ' | '.join(cells) + ' |')
    a('')
    a('## 5. Limits\n')
    a('1. **Two accounts, both successful, from one network.** Survivorship bias, and no failed accounts.')
    a('2. **Correlation, not cause.** Example: own-audio and original-file uploads are almost the same videos (19 of 22), so their separate effects can\'t be told apart.')
    a('3. **Timing isn\'t modelled.** Takeoff weeks and luck dominate absolute outcomes, so the 100K/1M probabilities move with the period they\'re trained on.')
    a(f'4. **Recent videos are excluded.** The newest {ACCRUAL_DAYS} days are dropped because those videos are still collecting views.')
    a('5. **Bootstrap ranges are not complete.** They reflect sampling noise only, not the bias in points 1–3.\n')
    with open(os.path.join(RESEARCH, 'success-model.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))


if __name__ == '__main__':
    main()
