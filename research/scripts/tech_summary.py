import json, sys, statistics as st
from collections import Counter
def rank(a):
    s = sorted(range(len(a)), key=lambda i: a[i]); r = [0]*len(a); i = 0
    while i < len(s):
        j = i
        while j+1 < len(s) and a[s[j+1]] == a[s[i]]: j += 1
        for k in range(i, j+1): r[s[k]] = (i+j)/2
        i = j+1
    return r
def spearman(x, y):
    rx, ry = rank(x), rank(y); n = len(x); mx, my = sum(rx)/n, sum(ry)/n
    num = sum((a-mx)*(b-my) for a, b in zip(rx, ry)); den = (sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))**0.5
    return num/den if den else float('nan')
for h in ['someplace505', 'elsewhere557']:
    v = json.load(open(f'{sys.argv[1]}/data/{h}.tech.json'))
    for x in v:
        g = x['gears']
        x['max_h'] = max((q['h'] or 0) for q in g) if g else 0
        x['max_fps'] = max((q['fps'] or 0) for q in g) if g else 0
        x['max_kbps'] = max((q['bitrate'] or 0) for q in g)/1000 if g else 0
        srcs = [q['ufq_src'] for q in g if q['ufq_src'] is not None]
        x['src_q'] = srcs[0] if srcs else None
        x['audio_kbps'] = max((q['audio_kbps'] or 0) for q in g) if g else 0
        top = max(g, key=lambda q: (q['h'] or 0, q['bitrate'] or 0)) if g else None
        x['top_gear'] = top
    n = len(v)
    print(f'===== {h} ({n} videos)')
    print('  max resolution available:', dict(Counter(f"{x['max_h']}p" for x in v).most_common()))
    print('  max fps available:', dict(Counter(x['max_fps'] for x in v).most_common()))
    print('  HD flag true:', sum(1 for x in v if x['hd_flag']), '| definitions:', dict(Counter(x['definition'] for x in v)))
    print('  codecs offered:', dict(Counter(q['codec'] for x in v for q in x['gears']).most_common()))
    print('  gear counts per video:', dict(Counter(len(x['gears']) for x in v)))
    tk = [x['top_gear']['bitrate']/1000 for x in v if x['top_gear']]
    print(f"  top-tier bitrate kbps: median {st.median(tk):,.0f}  p10 {sorted(tk)[int(.1*len(tk))]:,.0f}  p90 {sorted(tk)[int(.9*len(tk))]:,.0f}")
    print('  top-tier codec/fps:', dict(Counter(f"{x['top_gear']['codec']} {x['top_gear']['fps']}fps {x['top_gear']['w']}x{x['top_gear']['h']}" for x in v if x['top_gear']).most_common(5)))
    defn = {'540p': 540, '720p': 720, '1080p': 1080, '2160p': 2160}
    for x in v: x['def_p'] = defn.get(x['definition'])
    for dname in ['540p', '720p', '1080p', '2160p']:
        s2 = [x['views'] for x in v if x['definition'] == dname]
        if s2: print(f"  upload definition {dname}: n={len(s2)} ({len(s2)/n:.0%}) median views {st.median(s2):,.0f}")
    nog = [x for x in v if not x['gears']]
    print('  videos with no tier list:', len(nog), 'their definitions', dict(Counter(x['definition'] for x in nog)), 'default bitrate median', st.median([x['default_bitrate']/1000 for x in nog if x['default_bitrate']]) if nog else '-')
    mk = [x['max_kbps'] for x in v if x['gears']]
    print(f"  highest bitrate of any tier kbps: median {st.median(mk):,.0f}  max {max(mk):,.0f}")
    db = [x['default_bitrate']/1000 for x in v if x['default_bitrate']]
    print(f"  default playback bitrate kbps: median {st.median(db):,.0f} (codec {Counter(x['default_codec'] for x in v).most_common(2)})")
    sq = [x['src_q'] for x in v if x['src_q'] is not None]
    vq = [x['vq'] for x in v if x['vq'] is not None]
    print(f"  TikTok source-quality score (ufq src): n={len(sq)} median {st.median(sq):.1f} p10 {sorted(sq)[int(.1*len(sq))]:.1f} p90 {sorted(sq)[int(.9*len(sq))]:.1f}")
    print(f"  TikTok VQScore: n={len(vq)} median {st.median(vq):.1f} p10 {sorted(vq)[int(.1*len(vq))]:.1f} p90 {sorted(vq)[int(.9*len(vq))]:.1f}")
    ld = [x['loudness'] for x in v if x['loudness'] is not None]
    print(f"  loudness LUFS-ish: n={len(ld)} median {st.median(ld):.1f} p10 {sorted(ld)[int(.1*len(ld))]:.1f} p90 {sorted(ld)[int(.9*len(ld))]:.1f}")
    print(f"  audio kbps (max tier): {dict(Counter(round(x['audio_kbps']) for x in v).most_common(4))}")
    views = [x['views'] for x in v]
    for name, key in [('max resolution', 'max_h'), ('max fps', 'max_fps'), ('top-tier bitrate', 'max_kbps'), ('VQScore', 'vq'), ('source quality', 'src_q'), ('loudness', 'loudness'), ('duration', 'duration'), ('upload definition', 'def_p')]:
        pairs = [(x[key], x['views']) for x in v if x[key] is not None and (x['gears'] or key not in ('max_h','max_fps','max_kbps'))]
        print(f"  Spearman(views, {name}) = {spearman([a for a,_ in pairs], [b for _,b in pairs]):+.2f} (n={len(pairs)})")
    # views by 60fps vs not / 1080 vs not
    for label, cond in [('1080p+60fps', lambda x: x['max_h'] >= 1920 and x['max_fps'] >= 60), ('other', lambda x: not (x['max_h'] >= 1920 and x['max_fps'] >= 60))]:
        s = [x['views'] for x in v if cond(x)]
        if s: print(f"  {label}: n={len(s)} median views {st.median(s):,.0f}")
    json.dump(v, open(f'{sys.argv[1]}/data/{h}.tech2.json', 'w'))
