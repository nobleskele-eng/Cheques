# Download the audio of the top sounds in a new_sounds_<date>.csv into audio/<date>/ (default: latest CSV, tier A, top 5).
# usage: python3 -I research/scripts/download_audio.py [csv] [N]
# Gets each sound's playUrl from the public creator item_list of the account that used it (same endpoint as pull_account.py),
# then fetches that one audio file. Other accounts' sounds only; nothing of @papercheques is fetched (rule 3).
# The first TikTok 403, challenge page or empty response stops everything, no retries (rule 4).
# A CDN host this cloud environment's network policy refuses is skipped and named, then the next file is tried.
# Files already in the folder are kept and not fetched again.
# For reference and editing to the beat. On TikTok, still add the sound in the app so the post joins that sound's page.
import csv, glob, json, os, re, subprocess, sys, time, datetime as dt, urllib.error, urllib.request, urllib.parse
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
INVIS = ''.join(map(chr, (0x3164, 0x2800, 0xFFF4, 0xFFFC, 0x200D, 0xFE0E)))
src = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob(f'{R}/research/data/sounds/new_sounds_*.csv'))[-1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 5
rows = [r for r in csv.DictReader(open(src, encoding='utf-8')) if r['tier'] in ('A','B')][:N]
date = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(src)).group(1)
OUT = f'{R}/audio/{date}'
os.makedirs(OUT, exist_ok=True)

def get(url, ref='https://www.tiktok.com/'):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': ref}), timeout=40)
    return r.read(), r.headers.get('Content-Type', '')

def play_urls(handle, want, oldest):
    """sound id -> playUrl for the wanted sounds, paging this account's item_list back to `oldest`."""
    html = get(f'https://www.tiktok.com/@{handle}')[0].decode('utf-8', 'replace')
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
    if not m or 'webapp.user-detail' not in m.group(1):
        raise RuntimeError(f'{handle}: profile page has no user data (challenge page or blocked)')
    sec = json.loads(m.group(1))['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']['user']['secUid']
    found, cursor = {}, 0
    while True:
        q = urllib.parse.urlencode({'aid': 1988, 'count': 15, 'cursor': cursor, 'type': 1, 'secUid': sec})
        body = get('https://www.tiktok.com/api/creator/item_list/?' + q, f'https://www.tiktok.com/@{handle}')[0]
        if not body: raise RuntimeError(f'{handle}: empty item_list response')
        j = json.loads(body); batch = j.get('itemList') or []
        for it in batch:
            mu = it.get('music') or {}
            if mu.get('id') in want and mu.get('playUrl'): found.setdefault(mu['id'], mu['playUrl'])
        if want <= set(found) or not batch or not j.get('hasMorePrevious') or min(int(i['createTime']) for i in batch) < oldest: break
        cursor = min(int(i['createTime']) for i in batch) * 1000 + 999; time.sleep(1.2)
    return found

def name(n, r):
    who = r['uploaded_by'].strip(' ' + INVIS) or 'blank-name account'
    s = r['title'] + (f" - {r['artist']}" if r['artist'] else '') if r['title'] else f'original sound by {who}'
    s = re.sub(f'[{INVIS}\\\\/:*?"<>|]+', '', s).strip()[:60].strip()  # Windows-safe
    return f"{n:02d} {s} {r['sound_link'].rsplit('-', 1)[1]}"

want = {}  # account -> {sound id: (rank, row)}
for n, r in enumerate(rows, 1):
    sid = r['sound_link'].rsplit('-', 1)[1]
    for a in r['accounts'].split('+'): want.setdefault(a, {})[sid] = (n, r)
old = list(csv.DictReader(open(f'{OUT}/sources.csv', encoding='utf-8'))) if os.path.exists(f'{OUT}/sources.csv') else []
done, stopped, refused = [d for d in old if os.path.exists(f"{OUT}/{d['file']}")], None, {}
got = {d['sound_link'].rsplit('-', 1)[1] for d in done}
try:
    for i, (a, w) in enumerate(want.items()):
        if i: time.sleep(3)
        need = {s for s in w if s not in got}
        if not need: continue
        oldest = min(dt.datetime.fromisoformat(w[s][1]['first_used']).replace(tzinfo=dt.timezone.utc).timestamp() for s in need) - 86400
        for sid, url in play_urls(a, need, oldest).items():
            n, r = w[sid]
            try: data, ctype = get(url)
            except urllib.error.URLError as e:
                if 'Tunnel connection failed' not in str(e.reason): raise
                refused[sid] = urllib.parse.urlsplit(url).hostname; continue  # environment proxy, not TikTok
            if not data: raise RuntimeError(f'{sid}: empty audio response')
            ext = 'm4a' if data[4:8] == b'ftyp' else 'mp3' if data[:3] == b'ID3' or data[:2] in (b'\xff\xfb', b'\xff\xf3', b'\xff\xf2') else 'bin'
            f = f'{OUT}/{name(n, r)}.{ext}'
            open(f, 'wb').write(data); got.add(sid)
            dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip()
            done.append(dict(rank=n, file=os.path.basename(f), seconds=dur and round(float(dur), 1), kb=len(data) // 1024,
                             used_by=a, sound_link=r['sound_link'], best_views=r['best_views'], median_rel=r['median_rel']))
            time.sleep(1.2)
except Exception as e:
    stopped = str(e)[:200]
with open(f'{OUT}/sources.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, ['rank', 'file', 'seconds', 'kb', 'used_by', 'sound_link', 'best_views', 'median_rel'], lineterminator='\n')
    w.writeheader(); w.writerows(sorted(done, key=lambda d: int(d['rank'])))
missing = [name(n, r) for n, r in enumerate(rows, 1) if r['sound_link'].rsplit('-', 1)[1] not in got]
print(json.dumps({'saved': [d['file'] for d in sorted(done, key=lambda d: int(d['rank']))], 'missing': missing, 'stopped': stopped,
                  'host_refused_by_environment': refused,
                  'folder': os.path.relpath(OUT, R)}, ensure_ascii=False))
