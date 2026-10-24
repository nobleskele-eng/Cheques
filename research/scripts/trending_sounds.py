# Weekly new-sounds list for the niche (Monday routine). Sounds only: no video content is analysed.
# usage: python3 -I research/scripts/trending_sounds.py [--offline] [handle ...]
# 1. Per network account: profile page once (secUid), then creator item_list newest first, stopping 42 days back.
#    Same public endpoints as pull_account.py. Never /video/<id> pages or files (rule 3).
#    The first 403, challenge page, empty response or connection error stops all pulling (rule 4); the list is built from what came in.
#    --offline re-reads the last pull from research/scratch/sounds/ instead (no network).
# 2. Groups posts by audio: TikTok's own song match when it has one (re-uploads of one song merge), else the sound id
#    (edits, voice-line mixes and other non-song audio stay as their own sound).
#    A sound is "new" when no network post used it before the 14-day window (this pull + every research/data/*_sounds.csv)
#    and @papercheques never used it.
# 3. Writes research/data/sounds/new_sounds_<date>.csv (history) and overwrites reports/sounds.md.
# Doesn't touch the rival CSVs. Song names come from the network's own library-track posts, else from Apple's public lookup
# (skipped when the environment blocks itunes.apple.com).
import csv, glob, json, os, re, sys, time, statistics as st, datetime as dt, urllib.request, urllib.parse
from collections import defaultdict
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D, OUTD, SCRATCH, REPORT = f'{R}/research/data', f'{R}/research/data/sounds', f'{R}/research/scratch/sounds', f'{R}/reports/sounds.md'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
NETWORK = ['someplace505', 'elsewhere557', 'anywhere557', 'kadzoo55871', '.aaapaathy', 'fang_w3', 'rvf5567']
LOOKBACK, WINDOW, MATURE_H = 42, 14, 48
os.makedirs(OUTD, exist_ok=True); os.makedirs(SCRATCH, exist_ok=True)
now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
T = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc)
day = lambda t: T(t).strftime('%Y-%m-%d')
INVIS = ''.join(map(chr, (0x3164, 0x2800, 0xFFF4, 0xFFFC, 0x200D, 0xFE0E)))  # filler characters in blank-name accounts
blank = lambda s: not (s or '').strip(' ' + INVIS)
GENERIC = re.compile(r'^(original sound|son original|som original|suono originale|origineel geluid|originalton|sunet original|'
                     r'audio originale|sonido original|âm thanh gốc|الصوت الأصلي)', re.I)

def get(url, ref=None):
    h = {'User-Agent': UA, **({'Referer': ref} if ref else {})}
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=40).read()

def pull(handle):
    html = get(f'https://www.tiktok.com/@{handle}').decode('utf-8', 'replace')
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
    if not m or 'webapp.user-detail' not in m.group(1):
        raise RuntimeError('profile page has no user data (challenge page or blocked)')
    user = json.loads(m.group(1))['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']['user']
    stop, items, cursor = now.timestamp() - LOOKBACK * 86400, {}, 0
    while True:
        q = urllib.parse.urlencode({'aid': 1988, 'count': 15, 'cursor': cursor, 'type': 1, 'secUid': user['secUid']})
        body = get('https://www.tiktok.com/api/creator/item_list/?' + q, f'https://www.tiktok.com/@{handle}')
        if not body: raise RuntimeError('empty item_list response')
        j = json.loads(body); batch = j.get('itemList') or []
        for it in batch:
            mu, s = it.get('music') or {}, it.get('statsV2') or it.get('stats') or {}
            dsp = {x.get('platform'): x for x in (mu.get('tt2dsp') or {}).get('tt_to_dsp_song_infos') or []}
            items[it['id']] = dict(handle=handle, video_id=it['id'], t=int(it['createTime']), views=int(s.get('playCount', 0)),
                sound_id=mu.get('id', ''), title=mu.get('title', ''), author=mu.get('authorName', ''), library=not mu.get('original'),
                own=mu.get('authorName') == user['nickname'], usable=(it.get('item_control') or {}).get('can_music_redirect', True),
                song=next((x.get('meta_song_id') for x in dsp.values() if x.get('meta_song_id')), ''),
                spotify=(dsp.get(3) or {}).get('song_id', ''), apple=(dsp.get(1) or {}).get('song_id', ''))
        if not batch or not j.get('hasMorePrevious') or min(int(it['createTime']) for it in batch) < stop: break
        nc = min(int(it['createTime']) for it in batch) * 1000 + 999
        if cursor and nc >= cursor: break
        cursor = nc; time.sleep(1.2)
    rows = sorted((x for x in items.values() if x['t'] >= stop), key=lambda x: x['t'])
    json.dump(dict(pulled=now.timestamp(), rows=rows), open(f'{SCRATCH}/{handle}.json', 'w'))
    return rows

offline = '--offline' in sys.argv
handles, posts, done, stopped = [a for a in sys.argv[1:] if a != '--offline'] or NETWORK, [], [], None
for i, h in enumerate(handles):
    try:
        if offline:
            j = json.load(open(f'{SCRATCH}/{h}.json')); now = T(j['pulled']); rows = j['rows']
        else:
            if i: time.sleep(3)
            rows = pull(h)
    except Exception as e:
        stopped = dict(at=h, reason=str(e)[:160], not_pulled=handles[i + 1:]); break
    posts += rows; done.append(f'{h} {len(rows)}')
if not posts: sys.exit(json.dumps({'done': done, 'stopped': stopped, 'error': 'nothing pulled, no report written'}))

# Baseline = each account's median views over posts at least 48 h old in the 42-day pull (needs 5+).
base = {}
for h in {p['handle'] for p in posts}:
    v = [p['views'] for p in posts if p['handle'] == h and (now - T(p['t'])).total_seconds() >= MATURE_H * 3600]
    base[h] = st.median(v) if len(v) >= 5 else None
for p in posts:
    p['rel'] = p['views'] / base[p['handle']] if base[p['handle']] else None
    p['key'] = p['song'] or 's' + p['sound_id']

# Old = the network used it before the window (this pull, plus sound ids and Spotify ids in the rival CSVs),
# or @papercheques already used it (Let Go and the rest of the current list).
w0 = now.timestamp() - WINDOW * 86400
old_keys = {p['key'] for p in posts if p['t'] < w0}
old_sounds, old_spotify = set(), set()
for f in glob.glob(f'{D}/*_sounds.csv'):
    if f.endswith('proven_sounds.csv'): continue
    ours = os.path.basename(f).startswith('papercheques')
    for r in csv.DictReader(open(f, encoding='utf-8')):
        if ours or r['posted_utc'] < T(w0).strftime('%Y-%m-%d %H:%M:%S'):
            old_sounds.add(r['sound_id']); old_spotify.add(r.get('spotify_track_id') or '')
old_spotify.discard('')

songs = defaultdict(list)
for p in posts:
    if p['t'] >= w0: songs[p['key']].append(p)
names = {}  # song key -> (title, artist) from a library-track post of the same song
for p in posts:
    if p['library'] and not blank(p['title']): names.setdefault(p['key'], (p['title'], p['author']))
apple_ids = {p['apple'] for u in songs.values() for p in u if p['apple'] and p['key'] not in names}
apple, lookup = {}, 'not needed'
if apple_ids:
    try:
        ids = sorted(apple_ids)
        for k in range(0, len(ids), 100):
            for r in json.loads(get('https://itunes.apple.com/lookup?id=' + ','.join(ids[k:k + 100])))['results']:
                apple[str(r.get('trackId'))] = (r.get('trackName', ''), r.get('artistName', ''))
        lookup = f'{len(apple)}/{len(apple_ids)} named'
    except Exception as e: lookup = f'Apple lookup unreachable ({type(e).__name__}), Spotify links only'

out = []
for key, u in songs.items():
    if key in old_keys or any(p['sound_id'] in old_sounds or p['spotify'] in old_spotify for p in u): continue
    scored = [p for p in u if p['rel'] is not None]
    best = max(u, key=lambda p: (p['rel'] or 0, p['views']))
    nm = names.get(key) or next((apple[p['apple']] for p in u if p['apple'] in apple), None)
    if nm: title, artist = nm
    elif best['library']: title, artist = best['title'], best['author']
    elif blank(best['title']) or GENERIC.match(best['title']): title, artist = '', ''
    else: title, artist = best['title'], ''
    med = round(st.median(p['rel'] for p in scored), 2) if scored else None
    out.append(dict(song_key=key, title=title, artist=artist, uploaded_by='' if best['library'] else best['handle'] if best['own'] else best['author'],
        library_track=best['library'], uses=len(u), accounts='+'.join(sorted({p['handle'] for p in u})), best_views=best['views'],
        best_rel=round(best['rel'], 2) if best['rel'] else '', median_rel=med if med is not None else '',
        beat_baseline=f"{sum(p['rel'] > 1 for p in scored)}/{len(scored)}" if scored else '',
        first_used=day(min(p['t'] for p in u)), best_post_utc=T(best['t']).strftime('%Y-%m-%d %H:%M'),
        best_post_age_h=round((now - T(best['t'])).total_seconds() / 3600), sound_created=day(int(best['sound_id']) >> 32),
        usable=all(p['usable'] for p in u), sound_link=f"https://www.tiktok.com/music/x-{best['sound_id']}",
        spotify_link=f"https://open.spotify.com/track/{best['spotify']}" if best['spotify'] else '',
        other_sound_ids=' '.join(sorted({p['sound_id'] for p in u} - {best['sound_id']})),
        tier=''))
for r in out:  # A = several posts with a strong median; B = one big hit (could be the clip, not the sound)
    m, b = r['median_rel'] or 0, r['best_rel'] or 0
    if r['uses'] >= 2 and m >= 1.5 or r['accounts'].count('+') and b >= 2: r['tier'] = 'A'
    elif b >= 3 or r['best_views'] >= 1_000_000: r['tier'] = 'B'
    if r['library_track'] and r['uses'] >= 5 and m < 1: r['tier'] = 'promo?'
out.sort(key=lambda r: ({'A': 0, 'B': 1}.get(r['tier'], 2), -(r['median_rel'] or 0) if r['tier'] == 'A' else -(r['best_rel'] or 0), -r['best_views']))

snap = f"{OUTD}/new_sounds_{now:%Y-%m-%d}.csv"
prev = sorted(f for f in glob.glob(f'{OUTD}/new_sounds_*.csv') if f != snap)
last = {r['song_key'] for r in csv.DictReader(open(prev[-1], encoding='utf-8'))} if prev else set()
with open(snap, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, ['run_utc', *out[0]] if out else ['run_utc'], lineterminator='\n'); w.writeheader()
    for r in out: w.writerow({'run_utc': now.strftime('%Y-%m-%d %H:%M'), **r})

def label(r):
    u = r['uploaded_by']; who = '@' + u if u in NETWORK else 'a blank-name account' if blank(u) else u
    s = ' - '.join(x for x in (r['title'], r['artist']) if x) or 'original sound'
    if not r['library_track']: s += f' (upload by {who})' if r['title'] else f' by {who}'
    return re.sub(f'[{INVIS}]+', '', s).replace('|', '/').strip()
def row(n, r):
    flags = [x for x in ['accruing' if r['best_post_age_h'] < MATURE_H else '', 'repeat' if r['song_key'] in last else '',
                         'sound link off' if not r['usable'] else ''] if x]
    sp = f" · [Spotify]({r['spotify_link']})" if r['spotify_link'] else ''
    return (f"| {n} | {label(r)} | [sound]({r['sound_link']}){sp} | {r['uses']} ({r['accounts']}), {r['beat_baseline'].split('/')[0] or '?'} beat | "
            f"{r['best_views']:,} | {r['best_rel']}× | {r['median_rel']}× | {r['first_used'][5:]} | {', '.join(flags)} |")
A, B = [r for r in out if r['tier'] == 'A'][:8], [r for r in out if r['tier'] == 'B'][:8]
NONE = '| - | none this week | | | | | | | |'
hdr = '| # | Audio | Links | Uses, beat median | Best views | Best × | Median × | First used | Flags |\n|---|---|---|---|---|---|---|---|---|'
L = [f"# New sounds in the niche, {now:%Y-%m-%d} (trending_sounds.py, cloud)",
     f"Coverage, pulled {now:%Y-%m-%d %H:%M} UTC: {', '.join(done)} posts (last {LOOKBACK} d)." + (f" **Stopped at {stopped['at']}**: {stopped['reason']}; not pulled: {', '.join(stopped['not_pulled']) or 'none'}." if stopped else ''),
     f"New = no network post used the audio before {day(w0)} and @papercheques never used it. × = views / that account's median (posts ≥{MATURE_H} h old, last {LOOKBACK} d). Names: {lookup}.", '',
     '## A: spreading (2+ posts, median ≥1.5×, or 2+ accounts)', hdr, *([row(i + 1, r) for i, r in enumerate(A)] or [NONE]), '',
     '## B: one big hit (best ≥3× or 1M+, not repeated: may be the clip, not the sound)', hdr, *([row(i + 1, r) for i, r in enumerate(B)] or [NONE]), '',
     '## How to use',
     '- Open "sound" on your phone, then "Use this sound". An upload by another account is its "original sound".',
     '- If the sound page says unavailable, play the Spotify link and search that song in the TikTok sound library instead.',
     '- accruing = best post under 48 h old, × still rising. repeat = also on last week\'s list. Full table: ' + os.path.relpath(snap, R) + '.',
     f"- Skipped as likely paid promo (library track, 5+ uses, median <1×): {', '.join(label(r) for r in out if r['tier'] == 'promo?') or 'none'}."]
open(REPORT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(json.dumps({'done': done, 'stopped': stopped, 'new_songs': len(out), 'A': len(A), 'B': len(B), 'names': lookup, 'csv': os.path.relpath(snap, R)}))
