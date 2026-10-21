# Page through TikTok's creator item_list (newest -> oldest) and save compact records.
import json, re, sys, time, urllib.request, urllib.parse, os
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
handle, profile_html, out = sys.argv[1:4]
h = open(profile_html, encoding='utf-8', errors='replace').read()
d = json.loads(re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', h, re.S).group(1))
sec = d['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']['user']['secUid']
items, cursor, pages = {}, 0, 0
while True:
    q = urllib.parse.urlencode({'aid': 1988, 'count': 15, 'cursor': cursor, 'type': 1, 'secUid': sec})
    req = urllib.request.Request('https://www.tiktok.com/api/creator/item_list/?' + q,
                                 headers={'User-Agent': UA, 'Referer': f'https://www.tiktok.com/@{handle}'})
    body = urllib.request.urlopen(req, timeout=40).read()
    j = json.loads(body) if body else {}
    batch = j.get('itemList') or []
    pages += 1
    for it in batch:
        st = it.get('statsV2') or it.get('stats') or {}
        items[it['id']] = {
            'id': it['id'], 'createTime': it['createTime'], 'desc': it.get('desc', ''),
            'views': int(st.get('playCount', 0)), 'likes': int(st.get('diggCount', 0)),
            'comments': int(st.get('commentCount', 0)), 'shares': int(st.get('shareCount', 0)),
            'saves': int(st.get('collectCount', 0)), 'duration': it.get('video', {}).get('duration'),
            'music_title': it.get('music', {}).get('title'), 'music_original': it.get('music', {}).get('original'),
            'music_author': it.get('music', {}).get('authorName'), 'private': it.get('privateItem'),
            'isAd': it.get('isAd'), 'aigc': it.get('AIGCDescription'), 'lang': it.get('textLanguage'),
        }
    print(f'page {pages}: got {len(batch)}, total {len(items)}, hasMorePrevious={j.get("hasMorePrevious")}', file=sys.stderr)
    if not batch or not j.get('hasMorePrevious'):
        break
    new_cursor = min(it['createTime'] for it in batch) * 1000 + 999
    if cursor and new_cursor >= cursor:
        break
    cursor = new_cursor
    time.sleep(1.2)
json.dump(sorted(items.values(), key=lambda x: x['createTime']), open(out, 'w'))
print(json.dumps({'handle': handle, 'pages': pages, 'items': len(items)}))
