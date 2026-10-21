# Re-pull item_list keeping encoding/quality fields per video.
import json, re, sys, time, urllib.request, urllib.parse
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
handle, profile_html, out = sys.argv[1:4]
h = open(profile_html, encoding='utf-8', errors='replace').read()
d = json.loads(re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', h, re.S).group(1))
sec = d['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']['user']['secUid']
def jl(s):
    try: return json.loads(s) if s else {}
    except Exception: return {}
items, cursor = {}, 0
while True:
    q = urllib.parse.urlencode({'aid': 1988, 'count': 15, 'cursor': cursor, 'type': 1, 'secUid': sec})
    req = urllib.request.Request('https://www.tiktok.com/api/creator/item_list/?' + q, headers={'User-Agent': UA, 'Referer': f'https://www.tiktok.com/@{handle}'})
    body = urllib.request.urlopen(req, timeout=40).read(); j = json.loads(body) if body else {}
    batch = j.get('itemList') or []
    for it in batch:
        v = it.get('video', {}); st = it.get('statsV2') or it.get('stats') or {}
        gears = []
        for b in v.get('bitrateInfo') or []:
            pa = b.get('PlayAddr', {}); ex = jl(b.get('VideoExtra')); ufq = jl(ex.get('ufq'))
            gears.append(dict(gear=b.get('GearName'), codec=b.get('CodecType'), fps=b.get('BitrateFPS'), bitrate=b.get('Bitrate'),
                              w=pa.get('Width'), h=pa.get('Height'), size=pa.get('DataSize'), audio_kbps=(ex.get('audio_bit_rate') or 0)/1000,
                              ufq_src=ufq.get('src'), url=(pa.get('UrlList') or [None])[0]))
        vi = v.get('volumeInfo') or {}
        items[it['id']] = dict(id=it['id'], createTime=it['createTime'], views=int(st.get('playCount', 0)), likes=int(st.get('diggCount', 0)),
            duration=v.get('duration'), hd_flag=it.get('IsHDBitrate'), default_bitrate=v.get('bitrate'), default_codec=v.get('codecType'),
            definition=v.get('definition'), vq=float(v['VQScore']) if v.get('VQScore') else None, loudness=vi.get('Loudness'), peak=vi.get('Peak'),
            music_title=it.get('music', {}).get('title'), music_original=it.get('music', {}).get('original'), gears=gears)
    if not batch or not j.get('hasMorePrevious'): break
    cursor = min(it['createTime'] for it in batch) * 1000 + 999; time.sleep(1.2)
json.dump(sorted(items.values(), key=lambda x: x['createTime']), open(out, 'w'))
print(handle, len(items))
