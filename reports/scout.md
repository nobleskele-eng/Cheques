# Scout report (NATURE run, first with dyhook.js)
Run 2026-10-25 16:20-16:38 UTC. Douyin: 1 page load + ~18 in-page actions (searches, filters, clip modals, TA的作品 tabs). No stop signal: every captured response returned status 0. Screened from `tools/dyhook.js` data (272 clips); screenshots only for covers, frames, edges.

## Flag: p82 (READY, lite PASS)
The source creator 盐放多会咸 (1.2万 fans, 571 posts) uploaded this 虎跳峡 hike **3 times**: 7698960132067567481 (21 Oct, p82's source), 7699328997604443365 (22 Oct, 9.6 s, same spot and light) and 7700027963747860089 (24 Oct, 9.0 s, **same caption and same cover as p82** = a re-upload). The same week they posted from Iceland (19 Oct), Bangkok (13/15 Oct) and Dali (16 Oct), and they reuse captions across clips. So p82 fails the one-upload-per-shoot rule (the p54/p63 category), and it's unclear they shot it. Vyx decides: hold it, or post it and watch for an unoriginal flag.

## Picks (batch 2026-10-25; TikTok collision check not done)
1. **REJECTED by Vyx 25 Oct (no reveal, no subject, poor quality, slowed-down trend clip). owo · 7696867651759378368** · 3.9万 likes / 1,666 saves / 1.4万 shares · 11.4 s · 1080x1920 (top 1080P, 6.1 Mbps) · 15 Oct 12:17 UTC. Heavy snowfall at night over amber-lit flats in Urumqi, streetlamp and trees at the bottom, slow pan. Snow visible from 0.1 s (payoff in frame 1, no tilt-up). Luma 70-80. **City snow, not nature.**
   Creator: personal account (226 fans, 41 posts of dance practice and daily life); this is their one viral clip and the only upload of that snowfall. Signature: edgecheck clear (0) at 1080p, edges checked by eye at full res.
   Risks: shares 37% of likes and 10 days old, so it may already be on TikTok. Only 1080p. Caption is near 桑榆's p64 (same day, a local trend line; different footage).

## Rejected
- Nature words: default search gives old popular clips; 一周内 starves (峡谷徒步: 3).
- 湫 7699402396442771961 (5.7万, 7.8 s): saturated autumn-gold larches, under 8 s, shares 53%.
- 奶皮子的爸爸 7699055261496062449 (42.3万): 19.3 s, indoor window view.
- 屿城. 九寨沟 7696792580185797745 (38.4万): 70.7万-fan account, shares 63%, autumn colour.
- 阿略流浪记 / 靠谱的阳光 禾木 first snow (1.3万/1.1万): shares > likes.
- Gorge 推荐视频 (7): hiker as subject or far-off cloud sea. 领队/向导 accounts: guide businesses.

## Downloaded
- None. Next file number stays p85.

## Needs Vyx
- p82: hold or post (flag above). If it was posted on 24 Oct, watch it for an unoriginal flag.
- DM owo (`docs/methods.md` §3 text) if a city-snow clip is wanted now.

## Suggested MASTER changes
- §3/§6: p82 flag; owo = batch 2026-10-25 (A, city snow).
- methods §1: good word 新疆下雪了 (fresh vertical snow, this week). Bad: 沉浸式徒步 (all 17 are 42 s+ horizontal vlogs), 雪林 (mostly old or albums), 喀纳斯/稻城亚丁/雪山湖泊 (old popular).
- methods §2.5: edgecheck works on a live Douyin page with `__dy.src(id).url` as `src` (no 智能 menu needed).
