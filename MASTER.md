# MASTER: @papercheques current state
Updated 2026-10-24 by main (v22: new sounds, Monday routine). Cap 8,000 bytes. Tags: [L] local, [C] cloud, [V] Vyx, [est] estimate.

## 1. Where we are
- ~55 followers. 43 public posts, 3–24 Oct (cloud pull 24 Oct). Every post gets ~700 views (median 712, most 450–1,100): TikTok tests each one, but the test audience doesn't react. Best: 2,207 (10 Oct, waterfront walk-up reveal). [C]
- Our medians: 5.2% likes/view, 0.00% shares, 0.28% saves; like rate falling 6.3% (3–10 Oct) → 5.1% (11–16) → 4.2% (18–21). Network flops (<10K views): 8–11% likes, 0.6–1.1% shares. Breakouts (100K+): 21–25% likes, 2–4% shares (lifetime rates on 200K–380K accounts). [C] [L csv]
- Sourcing is good enough [V]: permissioned Douyin clips, and big accounts got millions from clips Vyx posted first. **Bottleneck = test-audience engagement.**
- FYP "unoriginal" flags: p53, p58, p59, p62. Account in good standing [V 19 Oct]. Raw reposts resumed, only after a Content check lite PASS.

## 2. What we know (strongest first)
1. **Content check lite** (TikTok Studio web upload) predicts flags: PASS → no flag 3/3 (p60, p64, p67). ERROR → p58 flagged, p54 never posted. Rejected: p65, p69, p73, p78, p79 (12–30 days old). Passed: p74–p77, so age/shares don't explain it. Weak lead (n=10): SaveTik H.264 passed 1 of 4, Douyin HEVC 4 of 6. [V][L ffprobe]
2. **Sound:** another account's sound mostly beats official tracks (1.24–1.53× vs 0.36–0.80× same-week views), but official "Let Go" (Ark Patrol) is elsewhere557's live hit: 8.1× over 8 uses. someplace505: own uploads 7.6× vs library tracks 0.8× (n=28/95; may be clip choice). 37/39 of ours use an account's sound, only 1 of 22 "proven" ones; n=3–8 per sound. [C]
3. **Served quality:** 0/43 of ours have a 1080p version (best 720p/1568k on p77, else 576p; views unchanged); the network gets 1080p on 81–99%, flops included. Our files are 1080p+, so the untested lever is the upload path: we use Studio web, peers likely the app with Upload HD [C 23 Oct, inference]. Brightness doesn't track views (p60, p64, p67). [C] [L gate]
4. **Openings:** all top 5 of the network's hit batch open on an upward reveal (tilt up from the ground or a railing). The 3 of ours checked are mostly static. n=8+3. [C]
5. **Length and cuts:** 23/39 of ours run 6–7 s; network hits 7–11 s, and 11–14 s+ did 1.1–2.0× (small n). [C] **Our clips get cut short between file and post:** 9 of 12 mapped posts since 5 Oct ended 6–9 s, 1.3–9.5 s shorter (median −3.0 s). Network lengths match their files. Full vs cut: no difference yet (certain n=3 vs 9: median 798 vs 709). [L ffprobe + csv]
6. **Volume:** views per post drop past ~3/day (someplace505) or ~6/day (elsewhere557). [C]
7. **Posting mode:** scheduled median 353 vs direct 716 (n=3 vs 36; 12 h ahead → 31 views). <10 min apart (n=4): 159–912; 42 min–2 h: ~700 each. Post directly, 40+ min apart. [L csv + decode]
8. **Hour (confounded):** 23:00–02:30 UTC (19:00–22:30 EDT) n=10: median 792, none <650, holds the top 4. 02:30–05:00 UTC n=19: median 687, 7 of 8 posts <600, but 6 of those 7 were scheduled or stacked. A test, not a rule. [L csv]
9. **The network is a business** (sound promo, €54.99 course). kadzoo55871 + elsewhere557 (+ anywhere557) = one operator; someplace505 likely separate. rvf5567 (22 Oct) very likely theirs (`reports/watch.md`). Hot phase ~1–3 weeks, then decay: elsewhere557 weekly median 102K (wk 28 Sep) → 26.3K → 23.2K (7 d, n44); kadzoo55871 slowed to 6 posts/wk. [C]
10. **Model** (`research/success-model.md`): 100K+ AUC 0.69, 1M+ 0.52. [C]

## 3. Recommendation now: change the recipe, then test it
Single-variable tests need dozens of posts at ~700 views, so run the likely levers together for ~10 posts, compare with the old 39, then remove levers one at a time. [est]
- **p80 next:** lite, post 24 Oct 19:00–22:30 EDT.
- **Upload-path test** on the next lite PASS: post from the TikTok app, Upload HD on, else p76 setup; check served tier in the next cloud pull (`research/replication-levers-and-encoding.md` §5).
- **Check length before Post:** the TikTok editor preview must show the file's full length. If it's shorter, stop and note the step.
- **Clip selection:** upward reveal, payoff in the first second, 8–13 s. **Post at full length.**
- **Recipe test [C 24 Oct]:** 3 scoreable (p74, p76, p77): median 730 views (old 39: 716), likes 3.9% (old 5.1%). Verdict too early; go to ~10. p81 (first upward reveal) still collecting.
- **p76 setup = default [V 22 Oct]:** original file, no edit, uncut, posted right after lite PASS. Edits unproven (p74 edit 2.3% vs p76 original 4.2%, n=1 each).
- **Sound** (`research/data/proven_sounds.csv`): Air 31.6× (stale), oscncs 19.2×, yuji 8.7×, Let Go 8.1×. Give each 2+ tries. Let Go: p74, p76, p77, p81; oscncs next. Skip likely paid promos (CIGARETTES, gambling). New sounds: `reports/sounds.md`.
- **Upload:** TikTok Studio web as drafts, "Upload HD" if offered, Content check lite must PASS. Post directly, never scheduled, 1–3/day, 40+ min apart. Credit the creator by the 抖音号 on their profile.
- **Log every post** in log.csv: tiktok_link, 1 h and 24 h views/likes, shares, saves, % For You, % watched to end.
- **First milestone:** any post ≥10–15% likes/view (network flop range). [est]

## 4. Open conflicts / unknowns
- **Dark charm vs compression:** charm v3 wants a dark muted grade, but at 540p / 0.5 Mbps dark footage turns to mush. Lifted-but-muted edits (e.g. YAVG 93→104) are untested on a live post. [L]
- **rvf5567 DM'd us 22 Oct:** "all your videos are reposted". True by design (permissioned reposts); likely a course-funnel opener [est]. Reply: ask which clips. [V]
- **Rivals data caveat:** item_list returned only 196 of elsewhere557; older rows merged back from git. The pull script overwrites, so it needs a fix. [C]
## 5. Waiting on Vyx
1. **p77:** full link. p74: edit or original?
2. **Who shortens clips:** you, or TikTok when the sound is added? Post at full length either way.
3. Map the 4 posts of 20–21 Oct (EDT 22:42, 23:24, 00:06, 02:00 sched.); p75 is one of the first three. Third lite reject: unknown. 雾必野 permission open.
4. rvf5567 DM: which clips did they name?
5. 韬 IFC: DM or skip? Drop 可爱到爆炸 (sells footage)?
6. **p61:** still unused? (HOLD, lite never run.)
7. **p81:** app or web? Full 10.8 s in preview? 1 h views/likes.

## 6. Pipeline
- Next file number: **p82**. Douyin: 13 of 20 loads used 24 Oct UTC; rest until 25 Oct.
- **New recipe [V 22 Oct]:**
  - **POSTED p74** (梁同学 train door, lifted edit) 21 Oct 23:25 EDT, "Let Go": 713 views, **2.2% likes**; 8 s (~1 s cut). [C pull]
  - **POSTED p76** (韬 HK rain, **original**, dark, lite instant PASS) 22 Oct 20:36 EDT, direct, "Let Go". 730 views, **4.1%**; 8 s, no cut. [C pull]
  - **POSTED p75** (谢景行 Dali lane) ~20–21 Oct, flopped: 706–718 views, 3.9–5.0% (which post: §5). [V][L]
  - **POSTED p77** (鱼丸三三 Wuwei snow, original, 11.3 s, lite instant PASS) ~22:52 EDT 22 Oct, direct, "Let Go": 24 h+: 737 views, 3.9% [C pull].
  - **POSTED p81** (梁同学 rain bridge tilt-up, original, uncut, lite PASS) 23 Oct 22:22 EDT, "Let Go". 11 h: 773 views, 5.2%, still collecting [C pull].
- **Used up: p50–p79** [V 23 Oct]: lite rejects in §2.1, the rest posted (one unclear).
- HOLD p61 (lite never run; §5). Never: p54, p63 (re-uploaded shoots), p55–p57 (baked signatures).
- **IN p80** (梁同学 dusk car window, bright, no reveal; precheck OK; lite not run).

## 7. Latest agent reports
- `reports/rivals.md` 24 Oct: Let Go 8.1×, network flat/decaying.
- `reports/self.md` 24 Oct: recipe n=3 flat; 21 Oct posts unmapped.
- `reports/scout.md` 24 Oct: 2 picks; stopped at load 10.
- `reports/gate.md` 22 Oct: p65–p72 checks.
- `reports/watch.md` (6-hourly to 5 Nov): rvf5567 tracker.
- `reports/sounds.md` 24 Oct (Mondays): unused new sounds + links.
