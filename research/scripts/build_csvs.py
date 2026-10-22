# Rebuild research/data/<handle>_{videos,encoding,sounds}.csv from the three pull_*.py JSON outputs.
# usage: build_csvs.py handle items.json tech.json music.json [--keep-old-encoding]
# Written 2026-10-22 (the original converter was never committed); validated against the 2026-10-21 CSVs.
import csv, json, sys, os, datetime as dt
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
handle, fi, ft, fm = sys.argv[1:5]
keep_enc = '--keep-old-encoding' in sys.argv
items, tech, music = json.load(open(fi)), {x['id']: x for x in json.load(open(ft))} if ft != '-' else {}, json.load(open(fm))
nick = music['nickname']; mus = {x['id']: x for x in music['items']}
T = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
def w(name, cols, rows):
    with open(f'{D}/{handle}_{name}.csv', 'w', newline='', encoding='utf-8') as f:
        c = csv.writer(f, lineterminator='\n'); c.writerow(cols); c.writerows(rows)
w('videos', ['video_id','posted_utc','views','likes','comments','shares','saves','duration_s','sound_title','sound_is_original'],
  [[i['id'],T(i['createTime']),i['views'],i['likes'],i['comments'],i['shares'],i['saves'],i['duration'],i['music_title'],i['music_original']] for i in items])
def origin(x):
    own = x['music_author'] == nick; d = x['createTime'] - (int(x['music_id']) >> 32)
    if own and abs(d) <= 3600: return 'new sound created by this upload'
    if own: return 're-used its own earlier sound'
    return "picked another account's sound" if x['original'] else 'picked an official library track'
# TikTok's song-match fields flicker between pulls; keep an earlier positive match instead of losing it.
try: oldsnd = {r['video_id']: r for r in csv.DictReader(open(f'{D}/{handle}_sounds.csv', encoding='utf-8'))}
except FileNotFoundError: oldsnd = {}
rows = []
for i in items:
    x = mus.get(i['id'])
    if not x: continue
    ct = int(x['music_id']) >> 32; o = oldsnd.get(i['id'], {})
    rows.append([i['id'],T(i['createTime']),x['views'],x['music_id'],T(ct),round((x['createTime']-ct)/86400,2),x['music_title'],x['music_author'],
                 origin(x),not x['original'],x['matched_song'] or o.get('matched_commercial_song') == 'True',x['spotify_id'] or o.get('spotify_track_id', '')])
w('sounds', ['video_id','posted_utc','views','sound_id','sound_created_utc','sound_age_days_at_post','sound_title','sound_author','sound_origin','official_library_track','matched_commercial_song','spotify_track_id'], rows)
if not keep_enc:
    ER = []
    for i in items:
        t = tech.get(i['id'])
        if not t: continue
        g = t['gears']; orig = not g
        b = max(g, key=lambda q: ((q['w'] or 0)*(q['h'] or 0), q['bitrate'] or 0)) if g else None
        ER.append([t['id'],T(t['createTime']),t['views'],orig,len(g),b and b['gear'] or '',b and b['codec'] or '',b and f"{b['w']}x{b['h']}" or '',
                   b and b['fps'] or '',b and round(b['bitrate']/1000) or '',round((t['default_bitrate'] or 0)/1000),t['vq'] or '',
                   next((q['ufq_src'] for q in g if q['ufq_src']), ''),t['loudness'] if t['loudness'] is not None else '',t['music_title']])
    w('encoding', ['video_id','posted_utc','views','original_file_served','tiers','best_tier','best_tier_codec','best_tier_res','best_tier_fps','best_tier_kbps','default_kbps','tiktok_vq_score','source_quality_score','loudness','sound_title'], ER)
print(handle, len(items), 'videos')
