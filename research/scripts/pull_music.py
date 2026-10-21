# Pull per-video sound metadata: sound id (creation time), author, original/commercial flags, matched song ids.
import json, re, sys, time, urllib.request, urllib.parse
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
handle, profile_html, out = sys.argv[1:4]
h = open(profile_html, encoding='utf-8', errors='replace').read()
d = json.loads(re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', h, re.S).group(1))
user = d['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']['user']
sec = user['secUid']
items, cursor = {}, 0
while True:
    q = urllib.parse.urlencode({'aid': 1988, 'count': 15, 'cursor': cursor, 'type': 1, 'secUid': sec})
    req = urllib.request.Request('https://www.tiktok.com/api/creator/item_list/?' + q, headers={'User-Agent': UA, 'Referer': f'https://www.tiktok.com/@{handle}'})
    body = urllib.request.urlopen(req, timeout=40).read(); j = json.loads(body) if body else {}
    batch = j.get('itemList') or []
    for it in batch:
        m = it.get('music', {}); st = it.get('statsV2') or it.get('stats') or {}
        dsp = (m.get('tt2dsp') or {}).get('tt_to_dsp_song_infos') or []
        items[it['id']] = dict(id=it['id'], createTime=it['createTime'], views=int(st.get('playCount', 0)),
            music_id=m.get('id'), music_title=m.get('title'), music_author=m.get('authorName'), original=m.get('original'),
            copyrighted=m.get('isCopyrighted'), commerce=m.get('is_commerce_music'), music_duration=m.get('duration'),
            matched_song=bool(dsp), spotify_id=next((x.get('song_id') for x in dsp if x.get('platform') == 3), None))
    if not batch or not j.get('hasMorePrevious'): break
    cursor = min(it['createTime'] for it in batch) * 1000 + 999; time.sleep(1.2)
json.dump({'nickname': user['nickname'], 'items': sorted(items.values(), key=lambda x: x['createTime'])}, open(out, 'w'))
print(handle, len(items))
