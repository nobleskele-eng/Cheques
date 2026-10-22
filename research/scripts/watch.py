# Watch tracker: run right after pull_account.py for the same handles. Keeps the growth curve that the pull overwrites.
# usage: python3 -I research/scripts/watch.py rvf5567 kadzoo55871   (first handle = the account being watched)
# 1. Appends this pull to research/data/watch/<handle>_snapshots.csv (posts <=14 days old) and <handle>_profile.csv.
# 2. Rewrites the data part of reports/watch.md. The "## Read" section (written by the watch routine) is kept as is.
# Reads only the CSVs and the profile page pull_account.py already saved; it makes no network requests.
import csv, json, os, re, sys, datetime as dt
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D, W, SCRATCH = f'{R}/research/data', f'{R}/research/data/watch', f'{R}/research/scratch'
REPORT = f'{R}/reports/watch.md'
OUR_MEDIAN, OUR_LIKES = 712, 5.2  # MASTER §1 (39 posts, 3-21 Oct)
os.makedirs(W, exist_ok=True)
now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
P = lambda s: dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').replace(tzinfo=dt.timezone.utc)
EDT = lambda t: (t - dt.timedelta(hours=4)).strftime('%a %d %b %H:%M')  # EDT until 1 Nov 2026
def rd(p):
    try: return list(csv.DictReader(open(p, encoding='utf-8')))
    except FileNotFoundError: return []
def add(p, cols, rows):
    new = not os.path.exists(p)
    with open(p, 'a', newline='', encoding='utf-8') as f:
        c = csv.writer(f, lineterminator='\n')
        if new: c.writerow(cols)
        c.writerows(rows)
pct = lambda a, b: f'{100 * int(a) / int(b):.1f}%' if int(b) else '-'

def profile(h):
    try: html = open(f'{SCRATCH}/{h}.html', encoding='utf-8').read()
    except FileNotFoundError: return None
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
    ui = json.loads(m.group(1))['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']
    u, s = ui['user'], ui.get('statsV2') or ui['stats']
    return {'followers': s['followerCount'], 'following': s['followingCount'], 'likes': s['heartCount'], 'videos': s['videoCount'],
            'nickname': u['nickname'].encode('unicode_escape').decode(), 'bio': u['signature'].replace('\n', ' / '),
            'bio_link': (u.get('bioLink') or {}).get('link', ''), 'language': u.get('language', ''),
            'created_utc': dt.datetime.fromtimestamp(u['createTime'], dt.timezone.utc).strftime('%Y-%m-%d')}

# Which network accounts used each sound (cross-account reuse = coordination or a paid promo).
sound_users = {}
for f in os.listdir(D):
    if f.endswith('_sounds.csv') and f != 'proven_sounds.csv':
        for r in rd(f'{D}/{f}'): sound_users.setdefault(r['sound_id'], set()).add(f[:-11])
proven = {r['sound_id']: r for r in rd(f'{D}/proven_sounds.csv')}

out = {}
for h in sys.argv[1:]:
    vids, snd, enc = rd(f'{D}/{h}_videos.csv'), {r['video_id']: r for r in rd(f'{D}/{h}_sounds.csv')}, {r['video_id']: r for r in rd(f'{D}/{h}_encoding.csv')}
    pr = profile(h)
    if pr: add(f'{W}/{h}_profile.csv', ['pulled_utc', *pr], [[now.strftime('%Y-%m-%d %H:%M'), *pr.values()]])
    rows = []
    for v in vids:
        age = (now - P(v['posted_utc'])).total_seconds() / 3600
        if age > 14 * 24: continue
        s, e = snd.get(v['video_id'], {}), enc.get(v['video_id'], {})
        rows.append([now.strftime('%Y-%m-%d %H:%M'), v['video_id'], v['posted_utc'], round(age, 1), v['views'], v['likes'], v['comments'], v['shares'], v['saves'],
                     v['duration_s'], s.get('sound_id', ''), s.get('sound_title', v['sound_title']), s.get('sound_author', ''), s.get('sound_origin', ''),
                     e.get('best_tier_res', ''), e.get('tiers', ''), e.get('best_tier_kbps', '')])
    add(f'{W}/{h}_snapshots.csv', ['pulled_utc', 'video_id', 'posted_utc', 'age_h', 'views', 'likes', 'comments', 'shares', 'saves', 'duration_s',
                                   'sound_id', 'sound_title', 'sound_author', 'sound_origin', 'best_res', 'tiers', 'best_kbps'], rows)
    out[h] = (pr, vids, snd, enc)
    print(h, len(rows), 'recent posts snapshotted')

# ---- report (data part) ----
h = sys.argv[1]
pr, vids, snd, enc = out[h]
snaps = rd(f'{W}/{h}_snapshots.csv')
prof = rd(f'{W}/{h}_profile.csv')
first_seen = {}
for r in snaps: first_seen.setdefault(r['video_id'], r['pulled_utc'])
live = {v['video_id'] for v in vids}
gone = sorted({r['video_id'] for r in snaps} - live)
def at(vid, hours):  # views at the first snapshot taken at or after this age
    c = [r for r in snaps if r['video_id'] == vid and float(r['age_h']) >= hours]
    return c[0]['views'] if c else '-'

L = [f'# Watch: @{h} (live tracker)', f'Updated {now:%Y-%m-%d %H:%M} UTC by research/scripts/watch.py. Data: research/data/watch/. {len({r["pulled_utc"] for r in snaps})} pulls so far.', '']
if pr:
    L += [f'**Profile:** {pr["followers"]} followers, follows {pr["following"]}, {pr["likes"]} likes, {pr["videos"]} videos. Created {pr["created_utc"]}, app language "{pr["language"]}". '
          f'Bio: "{pr["bio"] or "(empty)"}"{" · link " + pr["bio_link"] if pr["bio_link"] else ""}.', '']
if len(prof) > 1:
    L += ['**Followers over time:** ' + ' → '.join(f'{r["followers"]} ({r["pulled_utc"][5:]})' for r in prof[-8:]), '']
L += [f'## Posts (newest first). Our baseline: median {OUR_MEDIAN} views, {OUR_LIKES}% likes/view (MASTER §1)',
      '| posted EDT | len | views now | @6h | @24h | @48h | likes | shares | saves | res | sound (author) | sound also used by |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
for v in sorted(vids, key=lambda v: v['posted_utc'], reverse=True)[:20]:
    s, e = snd.get(v['video_id'], {}), enc.get(v['video_id'], {})
    others = sorted(sound_users.get(s.get('sound_id'), set()) - {h})
    tag = f' PROVEN {float(proven[s["sound_id"]]["median_relative_views"]):.1f}x' if s.get('sound_id') in proven and proven[s['sound_id']]['proven'] == 'True' else ''
    L.append(f'| {EDT(P(v["posted_utc"]))} ({v["video_id"][-6:]}) | {v["duration_s"]} s | {v["views"]} | {at(v["video_id"], 6)} | {at(v["video_id"], 24)} | {at(v["video_id"], 48)} '
             f'| {pct(v["likes"], v["views"])} | {pct(v["shares"], v["views"])} | {pct(v["saves"], v["views"])} | {e.get("best_tier_res", "?")} '
             f'| {s.get("sound_title", v["sound_title"])} ({s.get("sound_author", "?")}){tag} | {", ".join(others) or "-"} |')
L += ['', '@6h/@24h/@48h = views at the first pull at or after that age ("-" = not reached yet or no pull in time). Shares/saves/likes are % of views.']
if gone: L += ['', f'**Deleted or hidden since first seen:** ' + ', '.join(f'{g} (first seen {first_seen[g]})' for g in gone)]
for o in sys.argv[2:]:
    opr, ovids, osnd, _ = out[o]
    rec = [v for v in sorted(ovids, key=lambda v: v['posted_utc'], reverse=True) if (now - P(v['posted_utc'])).days < 3]
    L += ['', f'## @{o}, last 3 days ({len(rec)} posts{", " + opr["followers"] + " followers" if opr else ""})']
    L += [f'- {EDT(P(v["posted_utc"]))} EDT · {v["duration_s"]} s · {v["views"]} views · {pct(v["likes"], v["views"])} likes · {osnd.get(v["video_id"], {}).get("sound_title", v["sound_title"])} ({osnd.get(v["video_id"], {}).get("sound_author", "?")})' for v in rec[:12]]

read = '## Read\n(none yet)\n'
if os.path.exists(REPORT):
    old = open(REPORT, encoding='utf-8').read()
    if '## Read' in old: read = old[old.index('## Read'):]
open(REPORT, 'w', encoding='utf-8').write('\n'.join(L) + '\n\n' + read)
print('wrote', REPORT)
