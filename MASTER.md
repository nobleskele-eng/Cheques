# MASTER: scenery accounts current state
Updated 2026-11-21 by cloud weekly (v61: reports 21 Nov, rival pull 1/7). Tags: [L] local, [C] cloud, [V] Vyx, [est] estimate.

## 1. Where we are
- 57 followers [L 16 Nov], 53 posts, median 739 [C 21 Nov]. To 12 Nov (51): median 743 views, 5.2% likes/view; 47/51 in 450–1,100. Best: 4,688 (p27, 10 Oct), 67% from Search (Edgerunners 2 hype). **Each post gets one test batch in <40 min, then stops:** 12 Nov posts had 704/751 at 38 min; older posts +0 views 7→12 Nov. Detail: `research/seed-cap-2026-11-11.md`. [L]
- Our medians: 0.00% shares, 0.28% saves. Likes help a little (top-third like rate 790 views vs 707, ρ 0.37, n50) but our 2–8% is below network flops (8–11%) and breakouts (21–25%, 2–4% shares). [C][L]
- Sourcing works [V]: permissioned Douyin clips. **Bottleneck = test-audience engagement.** Sound, length, reveal, timing, captions all changed; none moved the band. Fresh sources didn't help either (n=7; p81 0.6 d after its Douyin upload → 811). [L]
- **Studio [V 12 Nov] p98/p99:** ~98% For You; avg watch 35–36% of length; 4.9–6.6% watched full; most leave at 0:01, reveal or not. vs elmo breakout: watch ~0.8×, likes ~0.3×, shares ~0.1×. No account block. **No post has ever had a 2nd For You batch.**
- FYP "unoriginal" flags: p53, p58, p59, p62.

## 2. What we know (strongest first)
1. **Content check lite** (TikTok Studio web upload) predicts flags: PASS → no flag 3/3 (p60, p64, p67). ERROR → p58 flagged, p54 never posted. Rejected: p65, p69, p73, p78–p80, p84. Passed: p74–p77, p81, p82. Format: weak lead. [V][L ffprobe]
2. **Sound:** another account's sound mostly beats official tracks (1.24–1.53× vs 0.36–0.80× same-week views). "Let Go" faded to 1.5× (11 uses, 55% beat): no longer proven. "original sound - ren" 46×, 100%, 4 uses, 15 Nov; "hold the line" (official) 3.8×, 88% beat, 16 uses, 9 Nov; "Originalton" 7dievgssn 4.4×, 6 uses [C 21 Nov]. [C] Ours since 24 Oct 22:35 UTC: own audio (new sound per upload, named after our blank nickname). [L]
3. **Served quality: no lift [L].** Original-file posts median 778 (n=6); someplace505 original alone 0.81× (n=17). Not the cap. 15 Nov: 576p re-encodes again.
4. **Openings:** all top 5 of the network's hit batch open on an upward reveal (tilt up from ground/railing). The 3 of ours checked are mostly static. n=8+3. [C] **Theme:** someplace505 nature posts ~206K median vs city ~42K (n=4+4). [L grid]
5. **Length and cuts:** network hits 6–13 s. 9 of 12 mapped posts since 5 Oct were cut short between file and post (median −3.0 s); full vs cut: no difference (n=3 vs 9). [L]
6. **Volume:** views per post drop past ~3/day (someplace505) or ~6/day (elsewhere557). [C]
7. **Posting mode:** scheduled median 353 vs direct 716 (n=3 vs 36; 12 h ahead → 31 views). Post directly, 40+ min apart. [L csv + decode]
8. **Hour (confounded):** 23:00–02:30 UTC n=10: median 792; 02:30–05:00 UTC n=19: 687. [L csv]
9. **The network is a business** (sound promo, €54.99 course). kadzoo55871 + elsewhere557 (+ anywhere557, rvf5567 likely) = one operator; someplace505 separate. elsewhere557 median 12.9K (7 d, unripe; best 2.2M 5 Nov); someplace505 28K 7-d median, 3.8M hit 14 Nov [C 21 Nov]; .aaapaathy 8.6M hit 7 Nov, fang_w3 993K 10 Nov [C 14 Nov].
10. **Model** (`research/success-model.md`): AUC 0.64 beat-median, 1M+ at chance. [C]

## 3. Recommendation now: change the recipe, then test it
- **Recipe test, 14 posts since 22 Oct:** median 765 vs 721 baseline, 649–1,101 views, likes 4.9% vs 5.2%, max 7.9% [C 21 Nov].  Levers don't move the ~700 band.
- **Search captions: withdrawn [V 12 Nov].** p27's search tail was a trend spike (Edgerunners 2) with 4.9% likes and 3 followers; no place names in captions (they drive "where?" comments). Keep the credit line. Note §7.
- **Test batch = ~96% Canada [V Studio 12 Nov]** (p98/p99); p27 61% US, via search. **US test account @sylvanism_ [V 12 Nov]** (SF; AdsPower + US ISP proxy, web only, never phone); **may replace @papercheques [V 16 Nov]**. **Hold lifted, not a shadowban [L 16 Nov]:** p101 166 views, 15 Nov post 256, likes 8.4–9.0% (ours 3.6–5.2%) [n=2]; p100 3; p106 49 at 2 h. Batches < ours. **Studio: >70% US [V 16 Nov]**: batch region follows the account. 1–2/day there. Never-posted clips only; rule 3. Note §9. **No self-shot, outtakes, own edits or stock [V 19 Oct, 11 Nov].**
- **Clip selection:** upward reveal, payoff in the first second, 8–13 s (14.5–20 s: trimmed [V 25 Oct]). **Post at full length.** **Pivot [V 12 Nov]:** nature, little/no city, never Chongqing; one striking feature (lanterns, bubbles); 4K60 preferred. Never slowed-down clips; needs a subject; 2K+.
- **p76 setup = default [V 22 Oct]:** original file, no edit, uncut, posted right after lite PASS.
- **Sound** (`research/data/proven_sounds.csv`): try hold the line, oscncs, yuji, blank-name original, 2+ tries each. Let Go no longer proven. Skip likely paid promos (list in `reports/rivals.md`). New sounds: `reports/sounds.md`.
- **Upload:** lite must PASS. "Upload HD" on. Post directly, never scheduled, 1–3/day, 40+ min apart. Credit the creator by 抖音号.
- **Log every post** in log.csv: tiktok_link, 1 h and 24 h views/likes, shares, saves, % For You, % watched to end.

## 4. Open conflicts / unknowns
- **Audio [L 12 Nov]:** 9 Nov list (15) in `audio/2026-11-09`. Challenged: links via browser pane, then `download_audio.mjs <csv> AB <urls.json>`.
- **Pull [C 21 Nov]:** 1/7 (someplace505); stopped at elsewhere557 (RemoteDisconnected), others stale from 14 Nov. rvf5567 failed 14 Nov. [L 12 Nov] Python runs locally but TikTok challenges it; in-page item_list via the browser pane works.
## 5. Waiting on Vyx
0. **Credit missing** on all captions, both accounts, to 16 Nov (rule 2; DM promised it): add 抖音号. 9 Nov + 10 Nov posts: p-numbers?
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
11. **15 Nov:** "test" (20 views: why?) + #ocean = p105? @sylvanism_ 02:37 = p96 or p103? Its % For You?
12. **Next 6 clips to @sylvanism_?** See seed-cap §9.
## 6. Pipeline
- **In, precheck no red, lite next [L 13 Nov, permission V 13 Nov]:** p105–p116, 12 nature. Plan `reports/gate.md`: p110 left (p102, p105 [est] posted; p106, p107 on @sylvanism_). p108–p116: creator check + 抖音号 before posting.
- Next file **p117**. Douyin pane blocked (服务异常, 13 Nov). **Nature, in, precheck OK, lite next [L 13 Nov, permission V 12 Nov]:** p103 Erhai dusk pan 4K 10.7 s · p104 Lijiang snow mountain 2K 8.6 s.
- **In, precheck OK, lite next [L 8 Nov, permission V 8 Nov]:** p94 雾必野 fog river towers 4K 8.1 s · p95 古溪月 night crossing 8.4 s · p96 梁同学 sunset bridge 2K 10.7 s · p97 谢景行 Nanjing snow 2K 9.3 s, dark. Older city: p85–p90, p92, p93.
- **READY p82** (盐放多会咸 虎跳峡 tilt-up, nature, 9.6 s 1080p): lite PASS 24 Oct; flagged: hike uploaded 3×, Vyx decides. Lite FAILED: p80, p84.
- **POSTED** (detail log.csv): p74 717 · p76 741 · p77 745 · p81 802 (Let Go) · p98 746 · p99 780 (12 Nov) · p102 545 (15 Nov) [est].
- Used up: p50–p79 [V 23 Oct]; p100 [est], p101, p106, p107, +1 on @sylvanism_. HOLD p61. Never: p54, p63 (re-uploaded shoots), p55–p57, p83, p91 Anne (baked signatures).

## 7. Latest agent reports
- `reports/`: rivals 21 Nov (1/7 pulled) · self 21 Nov (53 posts, no lift) · scout 13 Nov (block stop) · sounds 16 Nov.
