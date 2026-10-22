# Perceptual-hash every cover; find near-duplicate footage between papercheques and the network.
import os, sys, glob
from PIL import Image
S = sys.argv[1]
def dhash(path, n=16):
    im = Image.open(path).convert('L').resize((n + 1, n), Image.LANCZOS)
    px = list(im.getdata()); bits = 0
    for r in range(n):
        for c in range(n):
            bits = (bits << 1) | (px[r * (n + 1) + c] > px[r * (n + 1) + c + 1])
    return bits
H = {}
for p in glob.glob(f'{S}/covers/*.jpg'):
    try: H[os.path.basename(p)[:-4]] = dhash(p)
    except Exception: pass
mine = {k: v for k, v in H.items() if k.startswith('papercheques_')}
net = {k: v for k, v in H.items() if not k.startswith('papercheques_')}
ham = lambda a, b: bin(a ^ b).count('1')
# calibration: distance distribution between unrelated network covers
import random; random.seed(0)
ks = list(net); rnd = sorted(ham(net[random.choice(ks)], net[random.choice(ks)]) for _ in range(3000))
print('random pairs (256-bit dHash): 1st pct', rnd[30], '5th pct', rnd[150], 'median', rnd[1500])
# within-network cross-account near-dupes
sp = {k: v for k, v in net.items() if k.startswith('someplace')}; el = {k: v for k, v in net.items() if k.startswith('elsewhere')}
cross = sum(1 for a in sp.values() if min(ham(a, b) for b in el.values()) <= 40)
print(f'someplace505 covers with a near-match (<=40 bits) on elsewhere557: {cross}/{len(sp)}')
res = []
for k, v in mine.items():
    best = min(net.items(), key=lambda kv: ham(v, kv[1]))
    res.append((ham(v, best[1]), k.split('_', 1)[1], best[0]))
res.sort()
for d, mid, other in res:
    print(f'{d:>4} bits  papercheques {mid}  closest: {other}')
