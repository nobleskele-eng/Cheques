// edgecheck.js - finds a creator signature baked into a clip: small white text near the edges,
// usually cursive (韬 "Tao" bottom-centre, Iuk / 7na. right-middle). At 480-540 px these are ~15 px
// wide and get missed, so never judge signatures from small frames.
//
// How: takes the darkest value of every pixel across 24 frames. The scene moves, so it goes dark;
// a signature stays put, so it stays white. Same method and thresholds as the signature flag in
// tools/precheck.ps1 (known signatures score 96-317, clean moving shots 0-13).
//
// Use (scout, on a Douyin video page in the logged-in pane):
//   paste this file with javascript_tool, then:  await __edge({show: true})
//   -> {verdict, score, spot, where, ...}
//      SIGNATURE = reject the clip.  LOOK = check the overlay crop by eye (static shots land here,
//      because lit windows stay put too).  clear = nothing found.
//   The overlay (top-left) shows the fixed-pixels image with a red box on the strongest spot, and the
//   real middle frame cropped there at full resolution. Screenshot it, then __edge.clear().
// Loads the video file again from the CDN (no extra Douyin page load). ~7 s for a 4K clip.
window.__edge = async function (opt) {
  opt = opt || {};
  const RED = 80, LOOK = 25, SPOT = 0.4, N = 24, CELL = 40;
  let src = opt.src;
  if (!src) {
    const vids = [...document.querySelectorAll('video')].filter(v => v.currentSrc && v.clientWidth > 0);
    vids.sort((a, b) => b.clientWidth * b.clientHeight - a.clientWidth * a.clientHeight);
    if (!vids.length) return { error: 'no playing video on this page' };
    src = vids[0].currentSrc;
  }
  const v = document.createElement('video');
  v.crossOrigin = 'anonymous'; v.muted = true; v.preload = 'auto'; v.src = src;
  await new Promise((ok, no) => { v.onloadedmetadata = ok; v.onerror = () => no(new Error('video load failed')); });
  const seek = t => new Promise(ok => { v.onseeked = ok; v.currentTime = t; });

  // 24 frames spread over the clip, short side 1080 (never upscaled), like precheck
  const k = Math.min(1, 1080 / Math.min(v.videoWidth, v.videoHeight));
  const w = Math.round(v.videoWidth * k / 2) * 2, h = Math.round(v.videoHeight * k / 2) * 2;
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d', { willReadFrequently: true });
  const m = new Uint8Array(w * h).fill(255);
  for (let i = 0; i < N; i++) {
    await seek((i + 0.5) * v.duration / N);
    g.drawImage(v, 0, 0, w, h);
    const d = g.getImageData(0, 0, w, h).data;   // throws if the CDN refuses CORS
    for (let p = 0, q = 0; p < m.length; p++, q += 4) {
      const y = (d[q] * 77 + d[q + 1] * 150 + d[q + 2] * 29) >> 8;
      if (y < m[p]) m[p] = y;
    }
  }

  // stroke pixel: white-ish (>=120) and >=40 brighter than the pixels 4 px away on both sides,
  // across or up-down (thin lines like handwriting, not the edge of a bright area).
  // score = most stroke pixels in any 80x80 spot in the edge band (outer 15% left/right, 12% top/bottom)
  const D = 4, T = 40;
  const cw = Math.ceil(w / CELL), ch = Math.ceil(h / CELL), cells = new Int32Array(cw * ch);
  const x0 = Math.floor(w * 0.15), x1 = Math.floor(w * 0.85), y0 = Math.floor(h * 0.12), y1 = Math.floor(h * 0.88);
  let all = 0;
  for (let y = D; y < h - D; y++) for (let x = D; x < w - D; x++) {
    const val = m[y * w + x]; if (val < 120) continue;
    const across = val - m[y * w + x - D] >= T && val - m[y * w + x + D] >= T;
    const updown = val - m[(y - D) * w + x] >= T && val - m[(y + D) * w + x] >= T;
    if (!across && !updown) continue;
    all++;
    if (x >= x0 && x < x1 && y >= y0 && y < y1) continue;
    cells[Math.floor(y / CELL) * cw + Math.floor(x / CELL)]++;
  }
  let score = 0, tx = 0, ty = 0;
  for (let cy = 0; cy < ch - 1; cy++) for (let cx = 0; cx < cw - 1; cx++) {
    const s = cells[cy * cw + cx] + cells[cy * cw + cx + 1] + cells[(cy + 1) * cw + cx] + cells[(cy + 1) * cw + cx + 1];
    if (s > score) { score = s; tx = (cx + 1) * CELL; ty = (cy + 1) * CELL; }
  }
  const sx = tx / w, sy = ty / h, spot = all ? score / all : 0;
  const where = (sy < 0.33 ? 'top' : sy > 0.67 ? 'bottom' : 'middle') + '-' + (sx < 0.33 ? 'left' : sx > 0.67 ? 'right' : 'centre');
  const verdict = score >= RED && spot >= SPOT ? 'SIGNATURE' : score >= LOOK ? 'LOOK' : 'clear';
  const out = { verdict, score, spot: +spot.toFixed(2), where: score ? where : '-', x: +sx.toFixed(2), y: +sy.toFixed(2), w: v.videoWidth, h: v.videoHeight };

  if (opt.show) {
    window.__edge.clear();
    const box = document.createElement('div');
    box.id = '__edgebox';
    box.style.cssText = 'position:fixed;left:8px;top:8px;z-index:2147483647;background:#111;padding:6px;display:flex;gap:6px;align-items:flex-start;font:12px sans-serif;color:#fff';
    // fixed-pixels image, 150 px wide (fits the 800x450 pane), red box on the strongest spot
    const s = 150 / w, a = document.createElement('canvas'); a.width = 150; a.height = Math.round(h * s);
    const t = document.createElement('canvas'); t.width = w; t.height = h;
    const tg = t.getContext('2d'), img = tg.createImageData(w, h);
    for (let p = 0, q = 0; p < m.length; p++, q += 4) { img.data[q] = img.data[q + 1] = img.data[q + 2] = m[p]; img.data[q + 3] = 255; }
    tg.putImageData(img, 0, 0);
    const ag = a.getContext('2d'); ag.drawImage(t, 0, 0, a.width, a.height);
    ag.strokeStyle = 'red'; ag.lineWidth = 2;
    ag.strokeRect((tx - CELL) * s, (ty - CELL) * s, 2 * CELL * s, 2 * CELL * s);
    // real middle frame at full resolution, cropped on that spot: 30% x 14% of the short side
    await seek(v.duration / 2);
    const S = Math.min(v.videoWidth, v.videoHeight), zw = Math.round(S * 0.3), zh = Math.round(S * 0.142);
    const zx = Math.max(0, Math.min(v.videoWidth - zw, Math.round(sx * v.videoWidth - zw / 2)));
    const zy = Math.max(0, Math.min(v.videoHeight - zh, Math.round(sy * v.videoHeight - zh / 2)));
    const z = document.createElement('canvas'); z.width = zw; z.height = zh;
    z.getContext('2d').drawImage(v, zx, zy, zw, zh, 0, 0, zw, zh);
    z.style.cssText = 'width:' + Math.min(420, zw) + 'px';
    const label = document.createElement('div');
    label.textContent = verdict + ' · score ' + score + ' · ' + out.where;
    const col = document.createElement('div'); col.append(label, z);
    box.append(a, col);
    document.documentElement.append(box);
  }
  v.removeAttribute('src'); v.load();
  return out;
};
window.__edge.clear = () => document.getElementById('__edgebox')?.remove();
