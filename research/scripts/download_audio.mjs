// Node port of download_audio.py for the local PC (no Python here). Same rules: other accounts' sounds only,
// first 403 / challenge page / empty response stops everything, files already in the folder are kept.
// usage: node research/scripts/download_audio.mjs [csv] [tiers=AB] [urls.json]
// urls.json = {sound_id: playUrl} collected in the logged-in browser pane (creator item_list, music.playUrl) when TikTok
// challenges this PC's direct profile requests (8 + 12 Nov). With it, no TikTok page is fetched; only the audio files.
import fs from 'fs'; import path from 'path'; import { execFileSync } from 'child_process'; import { fileURLToPath } from 'url';
const R = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36';
const dir = `${R}/research/data/sounds`;
const src = process.argv[2] || `${dir}/` + fs.readdirSync(dir).filter(f => /^new_sounds_.*\.csv$/.test(f)).sort().pop();
const tiers = process.argv[3] || 'AB';
const URLS = process.argv[4] ? JSON.parse(fs.readFileSync(process.argv[4], 'utf8').replace(/^﻿/, '')) : null;
const sleep = ms => new Promise(r => setTimeout(r, ms));
function parseCsv(t) { // quoted fields, BOM safe
  t = t.replace(/^﻿/, ''); const rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < t.length; i++) { const c = t[i];
    if (q) { if (c === '"') { if (t[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
    else if (c === '"') q = true; else if (c === ',') { row.push(f); f = ''; }
    else if (c === '\n') { row.push(f.replace(/\r$/, '')); rows.push(row); row = []; f = ''; } else f += c; }
  if (f || row.length) { row.push(f); rows.push(row); }
  const h = rows.shift(); return rows.filter(r => r.length === h.length).map(r => Object.fromEntries(h.map((k, i) => [k, r[i]])));
}
const rows = parseCsv(fs.readFileSync(src, 'utf8')).filter(r => tiers.includes(r.tier) && r.tier).map((r, i) => ({ ...r, n: i + 1 }));
const date = src.match(/(\d{4}-\d{2}-\d{2})/)[1]; const OUT = `${R}/audio/${date}`; fs.mkdirSync(OUT, { recursive: true });
async function get(url, ref = 'https://www.tiktok.com/') {
  const r = await fetch(url, { headers: { 'User-Agent': UA, Referer: ref } });
  if (!r.ok) throw new Error(`HTTP ${r.status} ${url.slice(0, 80)}`);
  return Buffer.from(await r.arrayBuffer());
}
async function playUrls(handle, want, oldest) {
  const html = (await get(`https://www.tiktok.com/@${handle}`)).toString('utf8');
  const m = html.match(/<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)<\/script>/s);
  if (!m || !m[1].includes('webapp.user-detail')) throw new Error(`${handle}: profile page has no user data (challenge page or blocked)`);
  const sec = JSON.parse(m[1]).__DEFAULT_SCOPE__['webapp.user-detail'].userInfo.user.secUid;
  const found = {}; let cursor = 0;
  for (;;) {
    const q = new URLSearchParams({ aid: 1988, count: 15, cursor, type: 1, secUid: sec });
    const body = await get('https://www.tiktok.com/api/creator/item_list/?' + q, `https://www.tiktok.com/@${handle}`);
    if (!body.length) throw new Error(`${handle}: empty item_list response`);
    const j = JSON.parse(body); const batch = j.itemList || [];
    for (const it of batch) { const mu = it.music || {}; if (want.has(mu.id) && mu.playUrl && !found[mu.id]) found[mu.id] = mu.playUrl; }
    const minT = Math.min(...batch.map(i => +i.createTime));
    if ([...want].every(s => found[s]) || !batch.length || !j.hasMorePrevious || minT < oldest) break;
    cursor = minT * 1000 + 999; await sleep(1200);
  }
  return found;
}
const nm = r => { const who = r.uploaded_by.replace(/[ㅤ⠀￴￼‍︎]/g, '').trim() || 'blank-name account';
  let s = r.title ? r.title + (r.artist ? ` - ${r.artist}` : '') : `original sound by ${who}`;
  s = s.replace(/[\\/:*?"<>|ㅤ⠀￴￼‍︎]+/g, '').trim().slice(0, 60).trim();
  return `${String(r.n).padStart(2, '0')} ${s} ${r.sound_link.split('-').pop()}`; };
const sid = r => r.sound_link.split('-').pop();
const want = {}; for (const r of rows) for (const a of r.accounts.split('+')) (want[a] ??= new Map()).set(sid(r), r);
const have = f => fs.readdirSync(OUT).some(x => x.endsWith(' ' + sid(f) + '.mp3') || x.endsWith(' ' + sid(f) + '.m4a'));
const got = new Set(rows.filter(have).map(sid)); const saved = []; let stopped = null;
try {
  let first = true;
  for (const [a, w] of Object.entries(want)) {
    const need = new Set([...w.keys()].filter(s => !got.has(s))); if (!need.size) continue;
    const oldest = Math.min(...[...need].map(s => Date.parse(w.get(s).first_used + 'T00:00:00Z') / 1000)) - 86400;
    if (!URLS) { if (!first) await sleep(3000); first = false; }
    const urls = URLS ? Object.fromEntries([...need].filter(s => URLS[s]).map(s => [s, URLS[s]])) : await playUrls(a, need, oldest);
    for (const [s, url] of Object.entries(urls)) {
      const r = w.get(s); const data = await get(url); if (!data.length) throw new Error(`${s}: empty audio`);
      const ext = data.slice(4, 8).toString() === 'ftyp' ? 'm4a' : 'mp3'; const f = `${OUT}/${nm(r)}.${ext}`;
      fs.writeFileSync(f, data); got.add(s); saved.push(path.basename(f)); await sleep(1200);
    }
  }
} catch (e) { stopped = String(e.message).slice(0, 200); }
const dur = f => { try { return (+execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', `${OUT}/${f}`]).toString()).toFixed(1); } catch { return ''; } };
const files = fs.readdirSync(OUT).filter(f => /\.(mp3|m4a)$/.test(f)).sort();
fs.writeFileSync(`${OUT}/sources.csv`, 'file,seconds,kb,sound_link\n' + files.map(f => { const r = rows.find(x => f.endsWith(' ' + sid(x) + path.extname(f)));
  return [`"${f}"`, dur(f), Math.round(fs.statSync(`${OUT}/${f}`).size / 1024), r?.sound_link ?? ''].join(','); }).join('\n') + '\n');
console.log(JSON.stringify({ saved, missing: rows.filter(r => !got.has(sid(r))).map(nm), stopped, folder: path.relative(R, OUT) }, null, 1));
