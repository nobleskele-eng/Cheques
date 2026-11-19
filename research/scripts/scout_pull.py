# Scouting pull for a new niche (written 19 Nov for @duskism / stretchtok): profile page once (stats + secUid),
# then the newest N pages (15 posts each) of the public creator item_list. Same endpoints and UA as pull_account.py,
# but keeps width/height, cover URL and image-post flag. Never opens /video/<id> pages or video files (rule 3).
# usage: python3 -I research/scripts/scout_pull.py OUTDIR PAGES handle [handle ...]
import json, os, re, sys, time, urllib.request, urllib.parse
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
out, pages = sys.argv[1], int(sys.argv[2])
for n, h in enumerate(sys.argv[3:]):
    if n: time.sleep(3)
    try:
        html = urllib.request.urlopen(urllib.request.Request(f'https://www.tiktok.com/@{h}', headers={'User-Agent': UA}), timeout=40).read().decode('utf-8', 'replace')
        m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
        ud = json.loads(m.group(1))['__DEFAULT_SCOPE__'].get('webapp.user-detail', {})
        if 'userInfo' not in ud:  # account gone/renamed/private: skip it, not a block
            print(h, 'no profile data (statusCode', ud.get('statusCode'), ')', flush=True); continue
        ui = ud['userInfo']
        u = ui['user']; rec = {'handle': h, 'nickname': u.get('nickname'), 'bio': u.get('signature'), 'createTime': u.get('createTime'),
                              'stats': ui.get('statsV2') or ui.get('stats'), 'items': []}
        cursor = 0
        for p in range(pages):
            q = urllib.parse.urlencode({'aid': 1988, 'count': 15, 'cursor': cursor, 'type': 1, 'secUid': u['secUid']})
            body = urllib.request.urlopen(urllib.request.Request('https://www.tiktok.com/api/creator/item_list/?' + q,
                   headers={'User-Agent': UA, 'Referer': f'https://www.tiktok.com/@{h}'}), timeout=40).read()
            j = json.loads(body) if body else {}
            batch = j.get('itemList') or []
            for it in batch:
                st = it.get('statsV2') or it.get('stats') or {}; v = it.get('video', {}); mu = it.get('music', {})
                rec['items'].append({'id': it['id'], 'createTime': it['createTime'], 'desc': it.get('desc', ''),
                    'views': int(st.get('playCount', 0)), 'likes': int(st.get('diggCount', 0)), 'comments': int(st.get('commentCount', 0)),
                    'shares': int(st.get('shareCount', 0)), 'saves': int(st.get('collectCount', 0)),
                    'duration': v.get('duration'), 'w': v.get('width'), 'h': v.get('height'), 'ratio': v.get('ratio'),
                    'cover': v.get('cover'), 'music_title': mu.get('title'), 'music_author': mu.get('authorName'),
                    'music_original': mu.get('original'), 'pinned': it.get('isPinnedItem'), 'imagePost': bool(it.get('imagePost'))})
            if not batch or not j.get('hasMorePrevious'): break
            cursor = min(it['createTime'] for it in batch) * 1000 + 999
            time.sleep(1.2)
        rec['items'] = list({i['id']: i for i in rec['items']}.values())  # page boundaries repeat one post
        json.dump(rec, open(os.path.join(out, f'{h}.json'), 'w'))
        s = rec['stats'] or {}
        print(h, 'followers', s.get('followerCount'), 'videos', s.get('videoCount'), 'pulled', len(rec['items']), flush=True)
    except Exception as e:
        print(json.dumps({'stopped_at': h, 'reason': str(e)[:200]})); sys.exit(1)
