# MASTER: @papercheques current state
Updated 2026-10-24 05:20 UTC by cloud session (v24: viewers = For You + Canadian; caption test next). Cap 8,000 bytes. Overwrite stale lines; old versions in git history. Tags: [L] local work, [C] cloud research, [V] Vyx, [est] estimate.

## 1. Where we are
- ~55 followers. 43 public posts, 3–23 Oct (cloud pull 24 Oct). Every post gets ~700 views (median 712; last 6: 701–752 whatever changed): TikTok tests each one, but the test audience doesn't react. Best: 2,575 (10 Oct, waterfront walk-up reveal). [C]
- Our medians: 5.2% likes/view, 0.00% shares, 0.28% saves; like rate falling 6.3% (3–10 Oct) → 5.1% (11–16) → 4.2% (18–21). Network flops (<10K views): 8–11% likes, 0.6–1.1% shares. Breakouts (100K+): 21–25% likes, 2–4% shares (lifetime rates on 200K–380K accounts; one peer post fits: elmo, 442.8K views, 22% likes, 4.1% shares, 2.1% saves [V screenshot]). [C] [L csv]
- Sourcing is good enough [V]: permissioned Douyin clips, and big accounts got millions from clips Vyx posted first. **Bottleneck = test-audience engagement.**
- FYP "unoriginal" flags: p53, p58, p59, p62. Account in good standing [V 19 Oct]. Reposts only after a Content check lite PASS.

## 2. What we know (strongest first)
1. **Content check lite** (TikTok Studio web upload) predicts flags: PASS → no flag 3/3 (p60, p64, p67). ERROR → p58 flagged, p54 never posted. Rejected: p65, p69, p73, p78, p79 (12–30 days old). Passed: p74–p77 (3–20 days, up to 16.3万 shares), so age/shares don't explain it. Weak lead (n=11): SaveTik H.264 files passed 1 of 4, Douyin page-stream HEVC 5 of 7. [V][L ffprobe]
2. **Sound:** another account's sound mostly beats official tracks (1.24–1.53× vs 0.36–0.80× same-week views), but official "Let Go" (Ark Patrol) is elsewhere557's live hit: 11.6× over 6 uses; 4 posts 17–20 Oct: 182K–5.3M. 37/39 of ours use an account's sound, only 1 of 22 "proven" ones; n=3–8 per sound. [C]
3. **Served quality:** 0/39 of ours have a 1080p version (best ~533 kbps, 540–720p); the network gets 1080p on 81–99%, flops included. Our files are 1080p+. App + Upload HD tried [V 24 Oct]; still 0/43 with 1080p (best 720p, 15/43) [C 24 Oct], so it looks account-level [est]. someplace505's raw 4K originals come from a third-party tool ("RTX Fury"): **banned, rule 5**; edge confounded with own sound; elsewhere557 hits millions without it (research §6) [C]
4. **Openings:** all top 5 of the network's hit batch open on an upward reveal (tilt up from the ground or a railing). The 3 of ours checked are mostly static. n=8+3. [C]
5. **Length and cuts:** 23/39 of ours run 6–7 s; network hits 7–11 s, and 11–14 s+ did 1.1–2.0× (small n). [C] **Cut short before posting:** 9 of 12 mapped posts (median −3.0 s); network lengths match their files. Full vs cut: no difference (n=3 vs 9: 798 vs 709). [L ffprobe + csv]
6. **Volume:** views per post drop past ~3/day (someplace505) or ~6/day (elsewhere557). [C]
7. **Posting mode:** scheduled median 353 vs direct 716 (n=3 vs 36; 12 h ahead → 31 views). <10 min apart (n=4): 159–912; 42 min–2 h: ~700 each. Post directly, 40+ min apart. [L csv + decode]
8. **Hour (confounded):** 19:00–22:30 EDT n=10: median 792, holds the top 4; 22:30–01:00 EDT n=19: 687, but most lows were scheduled or stacked. A test, not a rule. [L csv]
9. **The network is a business** (sound promo, €54.99 course). kadzoo55871 + elsewhere557 (+ anywhere557) = one operator; someplace505 likely separate. rvf5567 (22 Oct) very likely theirs (`reports/watch.md`). Hot phase ~1–3 weeks, then decay: elsewhere557 weekly median 102K (wk 28 Sep) → 20K (wk 19 Oct, partial). [C]
10. **Model** (`research/success-model.md`): ranks 100K+ (AUC 0.69), not 1M+ (0.51). [C]

## 3. Recommendation now (recipe bundle since 21 Oct)
- **Tried, no change [V 24 Oct]:** app + Upload HD, instant-payoff clips, trending/non-trending sounds, own footage (camp lake: ~600 views, 30 likes). Not reposting.
- **Gap = test size [C]:** someplace505's first 4 relaunch posts had our like rate (4–7%) but ~4,300 views each; post 5 broke out (research §2.7). No hidden penalty: p81 views are For You, mostly Canadian [V 24 Oct]. TikTok: same country = weak signal, finishing = strong (newsroom); with no strong signals we get a local test pool [est].
- **Next 5 posts: caption test [C]:** place/mood line + 2–3 interest hashtags (+ credit). Only 2/43 posts had captions: #1 2,575 (#cyberpunk) and #4 937 (#nightwalk #china), same night, n=2. Win = any post >1,100.
- **Check length before Post:** preview must show the full file length.
- **Clip selection:** upward reveal, payoff in the first second, 8–13 s. **Post at full length.**
- **p76 setup = default [V 22 Oct]:** original file, no edit, uncut, right after lite PASS.
- **Sound** (`research/data/proven_sounds.csv`): oscncs 18.8×, Let Go 11.6×, Cherry 10.4×, yuji 8.7×. Give each 2+ tries. Let Go: p74/76/81 ~700, p77 unknown; oscncs next. Skip likely paid promos (CIGARETTES, gambling).
- **Upload:** Studio draft → lite PASS → post directly (never scheduled), 1–3/day, 40+ min apart. Credit the creator's 抖音号.
- **Log every post** in log.csv: tiktok_link, 1 h and 24 h views/likes, shares, saves, % For You, % watched to end.
- **First milestone:** any post ≥10–15% likes/view (network flop range). [est]

## 4. Open conflicts / unknowns
- **Dark charm vs compression:** charm v3 wants a dark muted grade, but at 540p / 0.5 Mbps dark footage turns to mush. Lifted-but-muted edits (e.g. YAVG 93→104) are untested on a live post. [L]
- **rvf5567 DM'd us 22 Oct:** "all your videos are reposted". True by design (permissioned reposts); likely a course-funnel opener [est]. Reply: ask which clips. Source doubts: p62 (_青), Hana. [V]
## 5. Waiting on Vyx
1. **p77:** full link; 1 h views/likes. p74: edit or original?
2. **Who shortens clips:** you, or TikTok when the sound is added? Post at full length either way.
3. Map the 4 posts of 20–21 Oct (EDT 22:42, 23:24, 00:06, 02:00 sched.); p75 is one of the first three. Third lite reject: unknown. 雾必野 permission open.
4. rvf5567 DM: which clips did they name?
5. 韬 IFC: DM or skip? Drop 可爱到爆炸 (sells footage)?
6. **p61:** still unused? (HOLD, lite never run.)
7. Which posts used app + Upload HD? p80 posted? Where's the credit (41/43 captions empty)?

## 6. Pipeline
- Next file number: **p82**. Douyin: 13 of 20 loads used 24 Oct UTC; rest until 25 Oct.
- **New recipe [V 22 Oct]:**
  - **POSTED p74** (梁同学 train door, lifted edit) 21 Oct 23:25 EDT, "Let Go": 15 h 709 views, **2.3% likes**; 8 s (~1 s cut). [C pull]
  - **POSTED p76** (韬 HK rain, **original**, dark) 22 Oct 20:36 EDT, "Let Go". 50 min: 694 views, **4.2%**, 2 saves; 8 s, no cut. [C pull]
  - **POSTED p75** (谢景行 Dali lane) ~20–21 Oct, flopped: 706–718 views, 3.9–5.0% (which post: §5). [V][L]
  - **POSTED p77** (鱼丸三三 Wuwei snow, original, 11.3 s) ~22:52 EDT 22 Oct, "Let Go": 10 min: 19 likes [V].
  - **POSTED p81** (梁同学 rain bridge tilt-up, original) 23 Oct 22:22 EDT, "Let Go". ~2 h: 752 views, 5.2%, 3 shares, uncut, 540p only; avg watch 2.8 s, before the ~3 s payoff [V].
- **Used up: p50–p79** [V 23 Oct]: lite rejects in §2.1, the rest posted (one unclear).
- HOLD p61 (lite never run; §5). Never: p54, p63 (re-uploaded shoots), p55–p57 (baked signatures).
- **IN p80** (梁同学 dusk car window, bright, no reveal; precheck OK; lite not run).
- Seasonal lead: Yunnan 冬樱花, mid-Nov to Dec [est].
- Snow posts 0 for 4; no theme has beaten ~700. [C data]

## 7. Latest agent reports
- `reports/rivals.md` 22 Oct: "Let Go" live hit; decay continues.
- `reports/self.md` 22 Oct (local, 21 Oct csv): 9 of 12 clips cut; scheduled vs direct; hour split.
- `reports/scout.md` 24 Oct: 2 picks; stopped at load 10.
- `reports/gate.md` 22 Oct: p65–p72 checks.
- `reports/watch.md` (6-hourly to 5 Nov): rvf5567 tracker.
