# Download the best available tier of given videos and make a 4-frame contact sheet each (files deleted after).
import json, re, sys, subprocess, urllib.request, http.cookiejar, os
S, handle = sys.argv[1], sys.argv[2]; ids = sys.argv[3:]
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
get = lambda u: op.open(urllib.request.Request(u, headers={'User-Agent': UA, 'Referer': 'https://www.tiktok.com/'}), timeout=60)
for vid in ids:
    page = get(f'https://www.tiktok.com/@{handle}/video/{vid}').read().decode('utf-8', 'replace')
    d = json.loads(re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', page, re.S).group(1))
    v = d['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']['video']
    gears = v.get('bitrateInfo') or []
    url = max(gears, key=lambda q: (q['PlayAddr'].get('Height') or 0, q.get('Bitrate') or 0))['PlayAddr']['UrlList'][0] if gears else v['playAddr']
    fn = f'{S}/frames/{vid}.mp4'; open(fn, 'wb').write(get(url).read())
    info = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,avg_frame_rate,bit_rate', '-of', 'csv=p=0', fn], capture_output=True, text=True).stdout.strip()
    out = f'{S}/frames/{vid}.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', fn, '-vf', 'fps=1/2,scale=270:-2,tile=4x1', '-frames:v', '1', out])
    os.remove(fn)
    print(vid, info, out)
