# Pull every video's cover image URL and download covers (for duplicate-footage check).
import json, re, sys, time, urllib.request, urllib.parse, os
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
S = sys.argv[1]
os.makedirs(f'{S}/covers', exist_ok=True)
for handle in sys.argv[2:]:
    h = open(f'{S}/tt/{handle}.html', encoding='utf-8', errors='replace').read()
    sec = json.loads(re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', h, re.S).group(1))['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']['user']['secUid']
    cursor, n, got = 0, 0, 0
    while True:
        q = urllib.parse.urlencode({'aid': 1988, 'count': 15, 'cursor': cursor, 'type': 1, 'secUid': sec})
        j = json.loads(urllib.request.urlopen(urllib.request.Request('https://www.tiktok.com/api/creator/item_list/?' + q, headers={'User-Agent': UA, 'Referer': 'https://www.tiktok.com/'}), timeout=40).read() or b'{}')
        batch = j.get('itemList') or []
        for it in batch:
            fn = f"{S}/covers/{handle}_{it['id']}.jpg"
            url = it['video'].get('originCover') or it['video'].get('cover')
            if url and not os.path.exists(fn):
                try:
                    open(fn, 'wb').write(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://www.tiktok.com/'}), timeout=30).read()); got += 1
                except Exception as e:
                    pass
            n += 1
        if not batch or not j.get('hasMorePrevious'): break
        cursor = min(it['createTime'] for it in batch) * 1000 + 999; time.sleep(1.0)
    print(handle, 'videos', n, 'covers downloaded', got)
