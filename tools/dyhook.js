// dyhook.js - reads the clip data Douyin's own page already fetches in the logged-in pane, so the scout
// screens search results, 推荐视频 lists and profile grids from data instead of screenshots and page text.
// Every clip in a search, related list or profile grid comes with likes, saves, shares, comments, exact
// post time, length, the top stream resolution and bitrate, the full caption and the author's sec_uid.
//
// Endpoints and field names come from Evil0ctal/Douyin_TikTok_Download_API (src/dtk/platforms/douyin)
// and tamnd/douyin-cli (douyin/api.go), read 25 Oct. We don't run either: both get past Douyin's
// anti-bot wall by forging its request signatures (a_bogus) and minting identities, which we don't do.
// This file sends no requests of its own; it only copies JSON the page has already received.
//
// Use (scout, logged-in pane, any douyin.com page):
//   paste this file with javascript_tool once per page load; after a reload, eval(localStorage.__dyh).
//   __dy.start() at the start of a run, so __dy.q() only lists clips seen in this run.
//   Then search with the page's own search box, change filters, scroll, open clips: each response is
//   captured. A full page load (navigate) drops the hook and what that load fetched, so move around
//   inside the page (search box, filters, clicking clips) instead of navigating.
//   __dy.q({minLikes: 2000, days: 14, minS: 8, maxS: 14, skip: '<ids>'})  -> one line per clip, best first
//     other options: sort ('likes', 'saves', 'shares', 't'), n, via ('search', 'related', 'post'),
//     author (name, handle or sec_uid), all (include earlier runs), wide (include horizontal clips)
//   __dy.lib(['<id>', ...])  -> library.csv rows (tier, status, type, ownership, risks left blank)
//   __dy.src('<id>')  -> top-quality file URL + size (download only with a permission yes; URLs expire)
//   __dy.log  -> last responses (path, items, status). A non-zero status or empty body = stop signal.
// Rows are kept in localStorage (__dyrows, newest 800) so a reload doesn't lose them. __dy.clear() empties it.
(function main() {
  const KEY = '__dyrows', UKEY = '__dyusers', MAX = 800;
  const TAKE = /拿了留痕|随便拿|可以拿|原创素材/;
  const SELL = /素材|教学|课程|预设|接单|商用|LUT/i;
  const AI = /可灵|AI生成|AIGC|即梦|AI创作|ai视频|#ai(?![a-z])/i;
  const SLOW = /慢放|慢动作|慢镜头|放慢|慢速|倍速/;
  const KEEP = /search|related|aweme\/post|aweme\/detail|feed|profile/;
  const load = k => { try { return JSON.parse(localStorage.getItem(k) || '{}'); } catch (e) { return {}; } };
  const dy = window.__dy = window.__dy || {};
  const rows = dy.rows = load(KEY), users = dy.users = load(UKEY);
  dy.log = dy.log || [];
  dy.mark = Number(localStorage.getItem('__dymark') || 0);

  const wan = n => n >= 1e4 ? (n / 1e4).toFixed(1) + '万' : String(n || 0);
  const tier = (w, h) => { const s = Math.min(w || 0, h || 0); return s >= 2160 ? '4K' : s >= 1440 ? '2K' : s >= 1080 ? '1080P' : s ? s + 'p' : '?'; };
  const utc = t => new Date(t * 1000).toISOString().slice(0, 16).replace('T', ' ');

  dy.save = function () {
    const ids = Object.keys(rows);
    if (ids.length > MAX) ids.sort((a, b) => rows[a].at - rows[b].at).slice(0, ids.length - MAX).forEach(id => delete rows[id]);
    try { localStorage.setItem(KEY, JSON.stringify(rows)); localStorage.setItem(UKEY, JSON.stringify(users)); } catch (e) {}
  };

  dy.row1 = function (a, via, from) {
    if (!a || !a.aweme_id) return null;
    const v = a.video || {}, st = a.statistics || {}, au = a.author || {};
    let top = null;
    (v.bit_rate || []).forEach(g => {
      const p = g.play_addr || {}, px = (p.width || 0) * (p.height || 0), br = g.bit_rate || 0;
      if (!top || px > top.px || (px === top.px && br > top.br))
        top = { px, w: p.width, h: p.height, br, size: p.data_size || 0, url: (p.url_list || [])[0] || '' };
    });
    const pa = v.play_addr || {};
    const w = (top && top.w) || pa.width || v.width || 0, h = (top && top.h) || pa.height || v.height || 0;
    const desc = (a.desc || '').replace(/\s+/g, ' ').trim();
    const flags = [];
    if (TAKE.test(desc)) flags.push('take');
    if (SELL.test(desc)) flags.push('sell?');
    if (AI.test(desc)) flags.push('AI');
    if (SLOW.test(desc)) flags.push('slow?');
    if (a.images && a.images.length) flags.push('album');
    if (a.is_ads) flags.push('ad');
    if ((st.share_count || 0) > (st.digg_count || 0)) flags.push('shr>lk');
    if (w > h) flags.push('wide');
    return {
      id: String(a.aweme_id), t: a.create_time || 0, s: Math.round((v.duration || a.duration || 0) / 100) / 10,
      w, h, mbps: top && top.br ? Math.round(top.br / 1e5) / 10 : 0, size: top ? top.size : 0,
      url: top ? top.url : (pa.url_list || [])[0] || '',
      likes: st.digg_count || 0, saves: st.collect_count || 0, shares: st.share_count || 0, comments: st.comment_count || 0,
      author: au.nickname || '', uid: au.unique_id || au.short_id || '', sec: au.sec_uid || '', fans: au.follower_count || 0,
      desc, flags, cover: ((v.cover || v.origin_cover || {}).url_list || [])[0] || '', via, from: from || '', at: Date.now()
    };
  };

  dy.eat = function (url, text) {
    const path = ((url.match(/\/aweme\/v1\/web\/([a-z_\/]+)/) || [])[1] || '?').replace(/\/$/, '');
    const objs = [];
    try { objs.push(JSON.parse(text)); } catch (e) {
      // streamed responses: one JSON object per line, sometimes after a length prefix
      String(text || '').split('\n').forEach(l => { const i = l.indexOf('{'); if (i >= 0) try { objs.push(JSON.parse(l.slice(i))); } catch (e2) {} });
    }
    const list = [];
    let sc = objs.length ? undefined : 'not json', nil = '';
    objs.forEach(j => {
      if (!j || typeof j !== 'object') return;
      if (sc === undefined && j.status_code !== undefined) sc = j.status_code;
      if (j.search_nil_info) nil = 'nil';
      if (j.aweme_detail) list.push(j.aweme_detail);
      (j.aweme_list || []).forEach(x => list.push(x));
      (Array.isArray(j.data) ? j.data : []).forEach(d => {
        if (d && d.aweme_info) list.push(d.aweme_info);
        ((d && d.aweme_mix_info && d.aweme_mix_info.mix_items) || []).forEach(x => list.push(x));
      });
      const u = j.user;
      if (u && u.sec_uid && /profile\/other/.test(path)) users[u.sec_uid] = { name: u.nickname || '', uid: u.unique_id || u.short_id || '', fans: u.follower_count || 0, posts: u.aweme_count || 0, bio: (u.signature || '').replace(/\s+/g, ' ').slice(0, 120) };
    });
    const q = new URL(url, location.href).searchParams;
    const via = /search/.test(path) ? 'search' : /related/.test(path) ? 'related' : /aweme\/post/.test(path) ? 'post' : /detail/.test(path) ? 'detail' : path;
    const from = q.get('keyword') || q.get('sec_user_id') || (via === 'related' ? q.get('aweme_id') : '') || '';
    let n = 0;
    list.forEach(a => {
      const r = dy.row1(a, via, from);
      if (!r) return;
      const old = rows[r.id];
      rows[r.id] = old ? Object.assign({}, old, r, { via: old.via, from: old.from }) : r;
      n++;
    });
    if (n || KEEP.test(path)) {
      dy.log.push({ at: new Date().toISOString().slice(11, 19), path, n, sc: sc === undefined ? '-' : sc, len: (text || '').length, from, nil });
      if (dy.log.length > 40) dy.log.shift();
    }
    if (n || objs.some(j => j && j.user)) dy.save();
  };

  dy.start = function () { dy.mark = Date.now(); localStorage.setItem('__dymark', String(dy.mark)); return 'run started'; };

  dy.q = function (o) {
    o = o || {};
    const now = Date.now() / 1000;
    const skip = String(o.skip || '').match(/\d{15,20}/g) || [];
    const by = o.author ? String(o.author) : '';
    const list = Object.values(rows).filter(r =>
      (o.all || r.at >= dy.mark) && r.likes >= (o.minLikes || 0) &&
      (!o.days || now - r.t <= o.days * 86400) && (!o.minS || r.s >= o.minS) && (!o.maxS || r.s <= o.maxS) &&
      (o.wide || r.flags.indexOf('wide') < 0) && r.flags.indexOf('album') < 0 && r.flags.indexOf('ad') < 0 &&
      (!o.via || r.via === o.via) && (!by || r.author.indexOf(by) >= 0 || r.uid === by || r.sec === by) &&
      skip.indexOf(r.id) < 0);
    const key = o.sort || 'likes';
    list.sort((a, b) => b[key] - a[key]);
    const fans = r => r.fans || (users[r.sec] || {}).fans || 0;
    return {
      total: Object.keys(rows).length, matched: list.length,
      rows: list.slice(0, o.n || 30).map(r => [r.id, ((now - r.t) / 86400).toFixed(1) + 'd', r.s + 's',
        r.w + 'x' + r.h, wan(r.likes) + '♥', wan(r.saves) + '★', wan(r.shares) + '↗',
        r.author + (fans(r) ? ' ' + wan(fans(r)) : ''), r.flags.join(','), r.desc.slice(0, 40)].join(' | '))
    };
  };

  dy.lib = function (ids) {
    const c = x => '"' + String(x === undefined || x === null ? '' : x).replace(/"/g, '""') + '"';
    return [].concat(ids).map(id => {
      const r = rows[id];
      if (!r) return id + ': not captured';
      const f = r.fans || (users[r.sec] || {}).fans;
      return ['', '', r.id, 'https://www.douyin.com/video/' + r.id, r.author, f ? wan(f) : '?', r.desc, '',
        wan(r.likes), wan(r.saves), wan(r.shares), wan(r.comments), r.s,
        r.w + 'x' + r.h + ' (top offered: ' + tier(r.w, r.h) + (r.mbps ? ', ' + r.mbps + ' Mbps' : '') + ')',
        r.w > r.h ? 'horizontal' : 'vertical', utc(r.t), '', '', 'no'].map(c).join(',');
    }).join('\n');
  };

  dy.src = function (id) {
    const r = rows[id];
    if (!r) return id + ': not captured';
    return { url: r.url, res: r.w + 'x' + r.h + ' ' + tier(r.w, r.h), mb: Math.round(r.size / 1e5) / 10, cover: r.cover, age_min: Math.round((Date.now() - r.at) / 6e4) };
  };

  dy.clear = function () { for (const k in rows) delete rows[k]; for (const k in users) delete users[k]; dy.log.length = 0; dy.save(); return 'cleared'; };

  if (!window.__dyHooked) {
    window.__dyHooked = true;
    const RX = /\/aweme\/v1\/web\//;
    const feed = (u, t) => { try { window.__dy.eat(u, t); } catch (e) {} };
    const XP = XMLHttpRequest.prototype, open = XP.open, send = XP.send;
    XP.open = function (m, u) { this.__dyu = String(u); return open.apply(this, arguments); };
    XP.send = function () {
      if (RX.test(this.__dyu || '')) this.addEventListener('load', function () {
        const t = this.responseType === '' || this.responseType === 'text' ? this.responseText
          : typeof this.response === 'string' ? this.response : JSON.stringify(this.response);
        feed(this.__dyu, t);
      });
      return send.apply(this, arguments);
    };
    const f0 = window.fetch;
    window.fetch = function (input) {
      const u = typeof input === 'string' ? input : (input && input.url) || '';
      const p = f0.apply(this, arguments);
      if (RX.test(u)) p.then(r => r.clone().text()).then(t => feed(u, t)).catch(() => {});
      return p;
    };
  }
  try { localStorage.setItem('__dyh', '(' + main.toString() + ')()'); } catch (e) {}
  return 'dyhook ready: ' + Object.keys(rows).length + ' rows stored';
})();
