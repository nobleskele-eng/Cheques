# One command per weekly pull: profile page -> item_list (items, tech, music) -> research/data/<handle>_*.csv.
# usage: python3 -I research/scripts/pull_account.py handle [handle ...]
# Reads only public data: each profile page once (for secUid) and the creator item_list endpoint.
# It never opens /video/<id> pages or downloads video files, so it is safe for @papercheques (rule 3).
# Stops everything at the first block or error, with no retries (rule 4).
import json, os, re, subprocess, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(os.path.dirname(HERE), 'scratch')  # gitignored
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
os.makedirs(SCRATCH, exist_ok=True)

def run(script, *args):
    r = subprocess.run([sys.executable, '-I', os.path.join(HERE, script), *args], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f'{script} failed: {(r.stderr or r.stdout).strip().splitlines()[-1:]}')
    return r.stdout.strip()

done = []
for i, h in enumerate(sys.argv[1:]):
    if i: time.sleep(3)
    page = os.path.join(SCRATCH, f'{h}.html')
    try:
        html = urllib.request.urlopen(urllib.request.Request(f'https://www.tiktok.com/@{h}', headers={'User-Agent': UA}), timeout=40).read().decode('utf-8', 'replace')
        m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
        if not m or 'webapp.user-detail' not in m.group(1):
            raise RuntimeError('profile page has no user data (challenge page or blocked)')
        open(page, 'w', encoding='utf-8').write(html)
        f = {k: os.path.join(SCRATCH, f'{h}.{k}.json') for k in ('items', 'tech', 'music')}
        run('pull_items.py', h, page, f['items'])
        run('pull_music.py', h, page, f['music'])
        try:
            run('pull_tech.py', h, page, f['tech'])
            print(run('build_csvs.py', h, f['items'], f['tech'], f['music']))
        except RuntimeError as e:  # keep last week's encoding rows, then stop (rule 4)
            print(run('build_csvs.py', h, f['items'], '-', f['music'], '--keep-old-encoding'))
            done.append(f'{h} (videos + sounds only)')
            raise RuntimeError(f'encoding pull failed, kept old encoding rows ({e})')
        done.append(h)
    except Exception as e:
        print(json.dumps({'done': done, 'stopped_at': h, 'reason': str(e)[:200], 'not_pulled': sys.argv[1:][i + 1:]}))
        sys.exit(1)
print(json.dumps({'done': done}))
