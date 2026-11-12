# MASTER: @papercheques current state
Updated 2026-11-11 by local session (v42: 51 posts, still ~700 cap; own-footage test proposed). Tags: [L] local, [C] cloud, [V] Vyx, [est] estimate.

## 1. Where we are
- ~59 followers. 51 public posts, 3 Oct–12 Nov (local pull 12 Nov 03:30 UTC). Median 739 views, 5.2% likes/view; 47/51 in 450–1,100. Best: 4,682 (10 Oct). **Each post gets one test batch in <40 min, then stops:** 12 Nov posts had 704/751 at 38 min; older posts +0 views 7→12 Nov. Detail: `research/seed-cap-2026-11-11.md`. [L]
- Our medians: 0.00% shares, 0.28% saves. Likes help a little (top-third like rate 790 views vs 707, ρ 0.37, n50) but our 2–8% is below network flops (8–11%) and breakouts (21–25%, 2–4% shares). [C][L]
- Sourcing works [V]: permissioned Douyin clips. **Bottleneck = test-audience engagement.** Sound, length, reveal, timing, captions all changed; none moved the band. Never varied: footage source (all 51 = others' Douyin clips). [L]
- FYP "unoriginal" flags: p53, p58, p59, p62.

## 2. What we know (strongest first)
1. **Content check lite** (TikTok Studio web upload) predicts flags: PASS → no flag 3/3 (p60, p64, p67). ERROR → p58 flagged, p54 never posted. Rejected: p65, p69, p73, p78–p80, p84. Passed: p74–p77, p81, p82. Format: weak lead. [V][L ffprobe]
2. **Sound:** another account's sound mostly beats official tracks (1.24–1.53× vs 0.36–0.80× same-week views). "Let Go" faded to 1.5× (11 uses, 55% beat): no longer proven. "hold the line" (drifting., official) now proven: 2.0×, 67% beat, 15 uses, last 6 Nov. Others (stale 3–5 wk): oscncs 14.2× (3 uses), yuji 8.1× (5), 𝙈𝙃𝘾 6.8× (3), blank-name "original sound" 5.7× (4 uses; someplace505's own upload). n=3–15 per sound. [C]
3. **Served quality:** 0/51 of ours have a 1080p version (best 720p); network 81–99%, flops included. Upload path (app + Upload HD) still untested. [C][L]
4. **Openings:** all top 5 of the network's hit batch open on an upward reveal (tilt up from ground/railing). The 3 of ours checked are mostly static. n=8+3. [C] **Theme:** someplace505 nature posts ~206K median vs city ~42K (n=4+4, 21–24 Oct; `research/someplace505-nature-2026-10-24.md`). [L grid]
5. **Length and cuts:** 23/39 of ours run 6–7 s; network hits 6–13 s. **Our clips get cut short between file and post:** 9 of 12 mapped posts since 5 Oct ended 6–9 s, median −3.0 s. Full vs cut: no difference yet (n=3 vs 9). [L ffprobe + csv]
6. **Volume:** views per post drop past ~3/day (someplace505) or ~6/day (elsewhere557). someplace505 ~4/day, 7-day median 13.3K (n33) vs 24.7K prior. [C]
7. **Posting mode:** scheduled median 353 vs direct 716 (n=3 vs 36; 12 h ahead → 31 views). Post directly, 40+ min apart. [L csv + decode]
8. **Hour (confounded):** 23:00–02:30 UTC (19:00–22:30 EDT) n=10: median 792, none <650, top 4. 02:30–05:00 UTC n=19: median 687. [L csv]
9. **The network is a business** (sound promo, €54.99 course). kadzoo55871 + elsewhere557 (+ anywhere557, rvf5567 likely) = one operator; someplace505 separate. elsewhere557 median 24.6K (best 2.2M, 5 Nov, 7 s); someplace505 13.3K. Detail: `reports/rivals.md`. [C]
10. **Model** (`research/success-model.md`): beat-median AUC 0.66, 100K+ 0.71, 1M+ 0.51 (chance). [C]

## 3. Recommendation now: change the recipe, then test it
Run the likely levers together for ~10 posts, compare with the old 39, then remove one at a time. [est]
- **Recipe test, 12 posts since 22 Oct** (p74–p81 + 8 unmapped, incl. 9–12 Nov): 700–1,092 views, likes 2.2–7.9%. Verdict [L 11 Nov]: recipe levers don't move the ~700 band.
- **Own-footage test (proposed L 11 Nov, Vyx decides):** Vyx shoots 2–3 clips (night/rain, street level, tilt-up in 1st s, 8–10 s), posts from the app with Upload HD on, 40+ min apart, caption = place + mood. Any ≥1,500 views [est] → footage source is the cap.
- **Captions:** #fyp #viral #views say nothing about topic. Use place + mood words (only 2 topical ever: 4,682 and 978, both 10 Oct; n=2).
- **Signature check [V 24 Oct]:** scout runs `tools/edgecheck.js` before DMs; red = never post (methods §2.5).
- **Clip selection:** upward reveal, payoff in the first second, 8–13 s (14.5–20 s: trimmed [V 25 Oct]). **Post at full length.** **Pivot [V 25 Oct]:** city, sunset beaches, bubbles. Never slowed-down clips; needs a subject; 2K+.
- **p76 setup = default [V 22 Oct]:** original file, no edit, uncut, posted right after lite PASS. Edits unproven (p74 edit 2.2% vs p76 original 4.0%, n=1 each).
- **Sound** (`research/data/proven_sounds.csv`): try hold the line, oscncs, yuji, blank-name original, 2+ tries each. Let Go no longer proven. Skip likely paid promos (list in `reports/rivals.md`). New sounds: `reports/sounds.md`.
- **Upload:** lite must PASS. "Upload HD" on. Post directly, never scheduled, 1–3/day, 40+ min apart (12 Nov pair: 2.4 min). Credit the creator by 抖音号.
- **Log every post** in log.csv: tiktok_link, 1 h and 24 h views/likes, shares, saves, % For You, % watched to end.

## 4. Open conflicts / unknowns
- **Dark charm vs compression:** dark grade turns to mush at 540p; lifted edits untested live. [L]
- **Audio blocked [L 8 Nov]:** TikTok challenge at profile 1, 0 fetched. Next day: `node research/scripts/download_audio.mjs research/data/sounds/audio_list_2026-11-08.csv ABX`.
- **Pull fragile:** [C 7 Nov] stopped at kadzoo55871; kadzoo, .aaapaathy, fang_w3, rvf5567 data 27 Oct or older. [L 12 Nov] Python runs locally but TikTok challenges it; in-page item_list via the browser pane works.
## 5. Waiting on Vyx
0. **4 new posts** (UTC 9 Nov 02:50 · 10 Nov 04:18 · 12 Nov 02:54, 02:57): p-numbers, app or web? Studio: % For You, avg watch time, % watched full. Account status: any notice? Own-footage test: yes/no?
1. **p77:** full link. p74: edit or original?
2. **Who shortens clips:** you, or TikTok when the sound is added?
3. Map the 4 posts of 20–21 Oct (EDT 22:42, 23:24, 00:06, 02:00 sched.); p75 is one of the first three.
4. rvf5567 DM 22 Oct (likely course funnel [est]): which clips?
5. Drop 可爱到爆炸 (sells footage)?
6. **p61:** still unused? (HOLD, lite never run.)
7. **p81:** app or web? Full 10.8 s in preview? 1 h views/likes.
8. **p76:** "Tao" mark at bottom centre? (韬, like p83)
9. **p82:** posted? Time + sound.
10. **4 unmatched posts** (UTC 24 Oct 22:35 · 25 Oct 23:34 · 27 Oct 01:51 · 30 Oct 01:48): p-numbers + upload path?
## 6. Pipeline
- Next file **p102**. 22 older approved clips fail §3. **Direction [V 8 Nov]:** consider non-city settings too. To contact: 谢景行 Lijiang snow-mountain tilt-up (non-city B). Hua. Weihai: yes, not downloaded (stop signal; maybe deleted).
- **In, precheck OK, lite next [L 8 Nov, permission V 8 Nov]:** p94 雾必野 fog river towers 4K 8.1 s · p95 古溪月 night crossing 8.4 s · p96 梁同学 sunset bridge 2K 10.7 s · p97 谢景行 Nanjing snow 2K 9.3 s, dark · p98 1Soove. sunset sea gulls 4K 9.4 s (non-city; reveal ~2 s) · p99 雾必野 rainy bridge 8.2 s (check slow-mo once) · p100 Hua. rain street 9.8 s · p101 雾必野 rain crossing 8.0 s. Older: p85 sunset tilt-up · p86 Beijing dusk tilt-up · p87 Xinjiang snow edit (HDR) · p88 leafy tilt-up · p89 leaves crosswalk 7 s · p90 rain tree 6.8 s · p92 Seoul snow · p93 snow towers.
- **READY p82** (盐放多会咸 虎跳峡 tilt-up, nature, 9.6 s 1080p): lite PASS 24 Oct; flagged: hike uploaded 3×, Vyx decides. Lite FAILED: p80, p84.
- **POSTED, new recipe, "Let Go", direct** [C 7 Nov; detail log.csv]: p74 (lifted edit) 717 views, 2.2% · p76 741, 4.0% · p77 745, 3.9% · p81 802, 5.2%.
- Used up: p50–p79 [V 23 Oct]. HOLD p61. Never: p54, p63 (re-uploaded shoots), p55–p57, p83, p91 Anne (baked signatures).

## 7. Latest agent reports
- `reports/`: rivals 7 Nov (3/7 pulled) · self 7 Nov (47 posts) · scout 8 Nov (p94–p101 in; Gexian, ginkgo 0; stop signal) · sounds 2 Nov (Mondays) · watch 27 Oct (ended).
