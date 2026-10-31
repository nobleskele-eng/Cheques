# MASTER: @papercheques current state
Updated 2026-10-31 by weekly routine, cloud (v37: rivals+self 31 Oct folded; 4 unmatched posts, pull failure). Tags: [L] local, [C] cloud, [V] Vyx, [est] estimate.

## 1. Where we are
- ~55 followers. 47 public posts, 3 Oct–30 Oct (cloud pull 31 Oct). Median 722 views, 5.1% likes/view; most 450–1,100: TikTok tests each one, test audience doesn't react. Best: 4,565 (10 Oct 01:42 UTC, 10 s, 225 likes). No post >1,010 since. [C]
- Our medians: 0.00% shares, 0.28% saves; like rate fell 6.3% (3–10 Oct) → 4.2% (18–21). Last 4 posts (24 Oct–30 Oct) 4.3–8.0%, median 6.95%, best since 10 Oct. Flops (<10K): 8–11% likes; breakouts (100K+): 21–25% likes, 2–4% shares. [C]
- Sourcing is good enough [V]: permissioned Douyin clips. **Bottleneck = test-audience engagement.**
- FYP "unoriginal" flags: p53, p58, p59, p62. Account in good standing [V 19 Oct].

## 2. What we know (strongest first)
1. **Content check lite** (TikTok Studio web upload) predicts flags: PASS → no flag 3/3 (p60, p64, p67). ERROR → p58 flagged, p54 never posted. Rejected: p65, p69, p73, p78, p79, p80, p84. Passed: p74–p77, p81, p82, so age/shares don't explain it. SaveTik H.264 passed 1 of 4; Douyin HEVC fails too (p80, p84): format weak lead. [V][L ffprobe]
2. **Sound:** another account's sound mostly beats official tracks (1.24–1.53× vs 0.36–0.80× same-week views). Official "Let Go" faded: 8.1× → 2.1× (10 uses, 70% beat, last 27 Oct). Now: oscncs 13.9× (3 uses), yuji 8.4× (5), 𝙈𝙃𝘾 6.8× (3), blank-name "original sound" 5.7× (4 uses; someplace505's own upload). someplace505's 2.1M (28 Oct) used official "hold the line" (5 uses, 1.74×, unproven). n=3–10 per sound; may ride the clip. [C]
3. **Served quality:** 0/43 of ours had 1080p (best 720p, p77); the latest 3 posts have no tier data, 24 Oct post 540p. Network gets 1080p on 81–99%, flops included. Untested lever: upload path (we use Studio web, peers likely app + Upload HD; inference). [C] [L gate]
4. **Openings:** all top 5 of the network's hit batch open on an upward reveal (tilt up from ground/railing). The 3 of ours checked are mostly static. n=8+3. [C] **Theme:** someplace505 nature posts ~206K median vs city ~42K (n=4+4, 21–24 Oct; `research/someplace505-nature-2026-10-24.md`). [L grid]
5. **Length and cuts:** 23/39 of ours run 6–7 s; network hits 8–13 s. **Our clips get cut short between file and post:** 9 of 12 mapped posts since 5 Oct ended 6–9 s, median −3.0 s. Full vs cut: no difference yet (n=3 vs 9). [L ffprobe + csv]
6. **Volume:** views per post drop past ~3/day (someplace505) or ~6/day (elsewhere557). someplace505 now ~4/day, 7-day median 19.8K (n27). [C]
7. **Posting mode:** scheduled median 353 vs direct 716 (n=3 vs 36; 12 h ahead → 31 views). Post directly, 40+ min apart. [L csv + decode]
8. **Hour (confounded):** 23:00–02:30 UTC (19:00–22:30 EDT) n=10: median 792, none <650, top 4. 02:30–05:00 UTC n=19: median 687. [L csv]
9. **The network is a business** (sound promo, €54.99 course). kadzoo55871 + elsewhere557 (+ anywhere557, rvf5567 likely) = one operator; someplace505 separate. Decay: elsewhere557 weekly median 117K → 13.7K (n38; best 1.6M 27 Oct); kadzoo restarted, 6 posts, median 7.7K (was 179K); anywhere557 silent since 22 Oct. someplace505 steady ~20K with a 2.1M. [C]
10. **Model** (`research/success-model.md`): beat-median AUC 0.66, 100K+ 0.68, 1M+ 0.45 (chance). [C]

## 3. Recommendation now: change the recipe, then test it
Run the likely levers together for ~10 posts, compare with the old 39, then remove one at a time. [est]
- **Recipe test [C 31 Oct]:** matched p74, p76, p77, p81, n=4: median 743 views (old 712), likes 4.0% (old 5.2%), shares 0.07%. Too early; go to ~10. Four later posts use the blank-name sound (median 762, likes 6.95%) but are unmapped (§5). Milestone ≥10–15% likes/view: not hit (best 8.0%).
- **p82 flag [L 25 Oct]:** creator uploaded the hike 3×, fails one-upload. Vyx decides.
- **Upload-path test** on the next lite PASS: post from the TikTok app, Upload HD on; check served tier in the next cloud pull (`research/replication-levers-and-encoding.md` §5).
- **Signature check [V 24 Oct]:** scout runs `tools/edgecheck.js` before DMs (p83 had a tiny "Tao"); red = never post (methods §2.5).
- **Check length before Post:** editor preview must show the full length; if shorter, stop and note the step.
- **Clip selection:** upward reveal, payoff in the first second, 8–13 s (14.5–20 s: trimmed [V 25 Oct]). **Post at full length.** **Pivot [V 25 Oct]:** city, sunset beaches, bubbles. Never slowed-down clips; needs a subject; 2K+.
- **p76 setup = default [V 22 Oct]:** original file, no edit, uncut, posted right after lite PASS. Edits unproven (p74 edit 2.2% vs p76 original 4.0%, n=1 each).
- **Sound** (`research/data/proven_sounds.csv`): try oscncs, yuji, blank-name original, 2+ tries each. Let Go fading. Skip likely paid promos (list in `reports/rivals.md`). New sounds: `reports/sounds.md`.
- **Upload:** TikTok Studio web as drafts, "Upload HD" if offered, lite must PASS. Post directly, never scheduled, 1–3/day, 40+ min apart. Credit the creator by 抖音号.
- **Log every post** in log.csv: tiktok_link, 1 h and 24 h views/likes, shares, saves, % For You, % watched to end.

## 4. Open conflicts / unknowns
- **Dark charm vs compression:** dark grade turns to mush at 540p; lifted edits untested live. [L]
- **rvf5567 DM 22 Oct** ("all your videos are reposted"): likely course funnel [est]; §5.4.
- **Pull failure [C 31 Oct]:** `pull_account.py` died at .aaapaathy (`KeyError: 'userInfo'`, profile had no user data). .aaapaathy, fang_w3, rvf5567 not refreshed (data from 27 Oct). Needs a fix; item_list returns only the newest ~196.
- **Watch routine silent** since 27 Oct (no `watch:` entry in `reports/watch.md`).
## 5. Waiting on Vyx
1. **p77:** full link. p74: edit or original?
2. **Who shortens clips:** you, or TikTok when the sound is added?
3. Map the 4 posts of 20–21 Oct (EDT 22:42, 23:24, 00:06, 02:00 sched.); p75 is one of the first three. Third lite reject: unknown.
4. rvf5567 DM: which clips did they name?
5. Drop 可爱到爆炸 (sells footage)?
6. **p61:** still unused? (HOLD, lite never run.)
7. **p81:** app or web? Full 10.8 s in preview? 1 h views/likes.
8. **p76:** "Tao" mark at bottom centre? (韬, like p83)
9. **p82:** posted? Time + sound.
10. **4 unmatched posts** (UTC 24 Oct 22:35 · 25 Oct 23:34 · 27 Oct 01:51 · 30 Oct 01:48; 735/789/699/1,005 views, all blank-name original): which p-numbers (p82, p85–p93?) and which upload path (was 30 Oct app + Upload HD?). No links in log.csv.
## 6. Pipeline
- Next file **p94** (dyhook). All 28 "to contact" library clips approved [V 26 Oct]; 22 unused.
- **In, precheck OK, lite next:** p85 梁同学 sunset tilt-up 4K 8.4 s · p86 谢景行 Beijing dusk tilt-up 4K 8.6 s · p87 黑色泡沫 Xinjiang snow edit 12.5 s, HDR · p88 可爱到爆炸 leafy tilt-up 8.6 s · p89 可爱到爆炸 leaves crosswalk 7 s · p90 用户1529 rain tree 6.8 s · p92 轻轻 Seoul snow 8 s · p93 長樂 snow towers 8.6 s (p88/p92/p93 odd fps: check slow-mo).
- **READY p82** (盐放多会咸 虎跳峡 tilt-up, nature, 9.6 s 1080p): lite PASS 24 Oct, flagged (§3). Lite FAILED: p80, p84.
- **POSTED, new recipe [V 22 Oct], all "Let Go", direct** [C 31 Oct]: p74 (梁同学 train door, lifted edit, 8 s) 22 Oct UTC 717 views, 2.2% · p76 (韬 HK rain, original, dark) 741, 4.0% · p77 (鱼丸三三 Wuwei snow, original, 11.3 s) 745, 3.9% · p81 (梁同学 rain bridge tilt-up, uncut) 802, 5.2%.
- Used up: p50–p79 [V 23 Oct]. HOLD p61. Never: p54, p63 (re-uploaded shoots), p55–p57, p83, p91 Anne (baked signatures).

## 7. Latest agent reports
- `reports/`: rivals 31 Oct (4/7 pulled; elsewhere557 collapse, Let Go 2.1×) · self 31 Oct (47 posts, recipe n=4 flat, 4 unmapped) · scout 25 Oct · sounds 24 Oct (Mondays) · watch 27 Oct (silent since).
