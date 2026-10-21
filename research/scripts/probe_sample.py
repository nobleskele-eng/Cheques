# Download a sample of videos (best available tier), ffprobe them, delete the files.
import json, re, sys, random, subprocess, urllib.request, time, os, http.cookiejar
JAR = http.cookiejar.CookieJar(); OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(JAR))
S = sys.argv[1]
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
def get(url, ref='https://www.tiktok.com/'):
    return OPENER.open(urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': ref}), timeout=60)
def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,bit_rate:stream=codec_type,codec_name,profile,width,height,avg_frame_rate,bit_rate,sample_rate,channels', '-of', 'json', path], capture_output=True, text=True).stdout
    return json.loads(out)
rows = []
for h in ['someplace505', 'elsewhere557']:
    v = json.load(open(f'{S}/data/{h}.tech.json'))
    by = sorted(v, key=lambda x: -x['views'])
    random.seed(7)
    sample = by[:3] + by[-2:] + random.sample(by[3:-2], 5)
    if h == 'someplace505':
        nog = [x for x in v if not x['gears'] and x not in sample]
        sample += random.sample(nog, 2)
    for x in sample:
        try:
            page = get(f'https://www.tiktok.com/@{h}/video/{x["id"]}').read().decode('utf-8', 'replace')
            d = json.loads(re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', page, re.S).group(1))
            vid = d['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']['video']
            gears = vid.get('bitrateInfo') or []
            if gears:
                g = max(gears, key=lambda q: (q.get('PlayAddr', {}).get('Height') or 0, q.get('Bitrate') or 0))
                url, src = g['PlayAddr']['UrlList'][0], g.get('GearName')
            else:
                url, src = vid.get('playAddr') or vid.get('downloadAddr'), 'default playAddr'
            data = get(url).read()
            fn = f'{S}/vid/{x["id"]}.mp4'; open(fn, 'wb').write(data)
            p = probe(fn); os.remove(fn)
            vs = next(s for s in p['streams'] if s['codec_type'] == 'video'); au = next((s for s in p['streams'] if s['codec_type'] == 'audio'), {})
            num, den = vs['avg_frame_rate'].split('/'); fps = float(num)/float(den) if float(den) else 0
            rows.append(dict(handle=h, id=x['id'], views=x['views'], tier=src, gears_on_page=len(gears), codec=vs['codec_name'], res=f"{vs['width']}x{vs['height']}", fps=round(fps, 2),
                             video_kbps=round(int(vs.get('bit_rate', 0))/1000), total_kbps=round(int(p['format'].get('bit_rate', 0))/1000),
                             audio=f"{au.get('codec_name')} {au.get('profile','')} {round(int(au.get('bit_rate', 0))/1000)}kbps {au.get('channels')}ch", dur=round(float(p['format']['duration']), 1), mb=round(len(data)/1e6, 2)))
            print(json.dumps(rows[-1]))
        except Exception as e:
            print(h, x['id'], 'FAILED', type(e).__name__, str(e)[:120])
        time.sleep(1.5)
json.dump(rows, open(f'{S}/data/probe_sample.json', 'w'), indent=1)
