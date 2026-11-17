# usage: python3 -I research/scripts/caption_types.py research/data   (labels fit the 17 Nov pull of 104 posts; re-label if the pull changes)
# Caption type vs views x on @stayvyxed. Labels by Claude from the caption text (17 Nov):
# F = fan voice (opinion / question / reaction about a show, character or episode), L = lyric line,
# T = title (show x artist, song title, edit title), O = other (lab/collab/thanks/meta), A = ambiguous.
import csv, statistics as st, sys
lab = dict(enumerate("FTTTOTTTTTLTTFTTTTFLTFTOTTTFTTTOTTOFTTTTTOLLLLTTLTTTFTTOLFFFFFFFFLTOLTLLLOFOTLFFLOLALLLOOLLLOTTLLOLLLLLF"))
D = sys.argv[1]
v = sorted(csv.DictReader(open(f'{D}/stayvyxed_videos.csv', encoding='utf-8-sig')), key=lambda r: r['posted_utc'])
assert len(v) == len(lab), (len(v), len(lab))
rows = []
for i, r in enumerate(v):
    prev = [int(p['views']) for p in v[max(0, i - 10):i]]
    if len(prev) >= 5: rows.append((lab[i], int(r['views']) / st.median(prev), r['posted_utc'][:7]))
for k in 'FTLO':
    xs = sorted(x for l, x, _ in rows if l == k)
    if xs: print(k, f'n={len(xs)} median={st.median(xs):.2f}x  >=1x {sum(x>=1 for x in xs)}/{len(xs)}  >=3x {sum(x>=3 for x in xs)}/{len(xs)}  >=10x {sum(x>=10 for x in xs)}/{len(xs)}')
# same split restricted to posts outside Jan 2026 (JJK S3 cluster)
for k in 'FL':
    xs = sorted(x for l, x, m in rows if l == k and m != '2026-01')
    print(k, 'excl. Jan 2026', f'n={len(xs)} median={st.median(xs):.2f}x >=3x {sum(x>=3 for x in xs)}/{len(xs)}')
