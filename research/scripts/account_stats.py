# Scoreboard numbers for accounts.md, built from files pull_account.py already wrote. No network.
# usage: python3 -I research/scripts/account_stats.py handle [handle ...]
# Reads research/scratch/<handle>.html (profile: followers, likes, video count; same parsing as watch.py)
# and research/data/<handle>_videos.csv (views per post). Prints one JSON line per handle.
# Posts under 24 h old count as "still collecting": they're listed but left out of the medians.
import csv, json, os, re, statistics, sys, datetime as dt
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # research/
now = dt.datetime.now(dt.timezone.utc)

def profile(h):
    try:
        html = open(os.path.join(R, 'scratch', f'{h}.html'), encoding='utf-8').read()
        m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
        ui = json.loads(m.group(1))['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']
        s = ui.get('statsV2') or ui['stats']
        return {'followers': int(s['followerCount']), 'likes_total': int(s['heartCount']), 'videos_on_profile': int(s['videoCount'])}
    except Exception as e:  # no page saved (pull failed) or a different page shape
        return {'profile_error': f'{type(e).__name__}: {str(e)[:80]}'}

def posts(h):
    rows = []
    with open(os.path.join(R, 'data', f'{h}_videos.csv'), encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            try:
                t = dt.datetime.strptime(r['posted_utc'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=dt.timezone.utc)
                rows.append((t, int(r['views']), r['video_id']))
            except (ValueError, KeyError):
                continue
    return sorted(rows)

for h in sys.argv[1:]:
    out = {'handle': h, **profile(h)}
    try:
        rows = posts(h)
    except FileNotFoundError:
        rows = None
        out['posts_error'] = 'no videos csv (pull failed or never ran)'
    if rows:
        settled = [v for t, v, _ in rows if (now - t).total_seconds() >= 86400]
        this_year = [r for r in rows if r[0].year == now.year]
        best = max(this_year, key=lambda r: r[1]) if this_year else None
        day = lambda t: t.strftime('%Y-%m-%d %H:%M')
        out.update({
            'posts_in_pull': len(rows),
            'median_views_all': statistics.median(settled) if settled else None,
            'median_views_last10': statistics.median(settled[-10:]) if settled else None,
            'best_this_year': {'views': best[1], 'posted_utc': day(best[0]), 'video_id': best[2]} if best else None,
            'latest': {'views': rows[-1][1], 'posted_utc': day(rows[-1][0]), 'hours_old': round((now - rows[-1][0]).total_seconds() / 3600, 1)},
            'posts_last_7d': [{'posted_utc': day(t), 'views': v, 'still_collecting': (now - t).total_seconds() < 86400}
                              for t, v, _ in rows if (now - t).total_seconds() < 7 * 86400],
        })
    print(json.dumps(out, ensure_ascii=False))
