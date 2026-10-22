# MASTER: @papercheques current state
Updated 2026-10-21 by local session (v1: local notes + cloud research merged). Cap 8,000 bytes. Overwrite stale lines; old versions are in git history. Tags: [L] local work, [C] cloud research, [V] Vyx, [est] estimate.

## 1. Where we are
- ~55 followers. 39 public posts, 3–21 Oct. Every post gets ~700 views (median 712, most 450–1,100): TikTok tests each one, but the test audience doesn't react. Best: 2,207 (10 Oct, waterfront walk-up reveal). [C]
- Our medians: 5.2% likes/view, 0.00% shares, 0.28% saves. Network flops (<10K views): 8–11% likes, 0.6–1.1% shares. Breakouts (100K+): 21–25% likes, 2–4% shares. Network numbers are lifetime rates on 200K–380K accounts, so use them as direction only. [C]
- Sourcing is good enough [V]: permissioned Douyin clips, and big accounts got millions from clips Vyx posted first. **Bottleneck = test-audience engagement.**
- FYP "unoriginal" flags: p53, p58, p59, p62. Account in good standing [V 19 Oct]. Raw reposts resumed, but only after a Content check lite PASS.

## 2. What we know (strongest first)
1. **Content check lite** (TikTok Studio web upload) predicts flags: PASS → no flag 3/3 (p60, p64, p67). ERROR → p58 flagged, p54 never posted. n=5. [L]
2. **Sound:** picking another account's uploaded sound beats official library tracks (1.24–1.53× vs 0.36–0.80× same-week views on the network). 37/39 of ours already pick an account's sound, but only 1 of the 22 "proven" sounds. That alone hasn't moved us off ~700. [C replication-levers §2]
3. **Served quality:** 0/39 of our posts have a 1080p version (best ~533 kbps, 540–720p). The network gets 1080p on 81–99% of posts, at every view level, flops included. Our upload quality scores are similar (74.4 vs 75.9–77.4). Cause or effect is unknown. [C]
4. **Openings:** all top 5 of the network's hit batch open on an upward reveal (tilt up from the ground or a railing). The 3 of ours checked are mostly static. n=8+3. [C]
5. **Length:** 23/39 of ours run 6–7 s. Network hits run 7–11 s; 11–14 s+ did 1.1–2.0× (small n). [C]
6. **Volume:** views per post drop past ~3/day (someplace505) or ~6/day (elsewhere557). [C]
7. **Cold start:** someplace505's first 4 posts after its relaunch stalled at ~4.3K. Post 5 broke out (24% likes) on its 2nd try of a sound that had failed once. One account, so it's an example, not a rule. [C]
8. **Scheduling:** video ID time ≠ post time means the post was scheduled. Scheduled 12 h ahead → 31 views, 3.5 h → 353, 1.9 h → 690. Direct posts ~700. n=3: post directly. [C data + L decode]
9. **Spacing:** the four 21 Oct posts (42 min–2 h apart) each got ~700, so the "p67 lost its audience to p64" idea is weak. [C data]
10. **The network is a business:** sound promo plus a €54.99 course. kadzoo55871 + elsewhere557 (+ anywhere557) = one operator. someplace505 = likely a separate person on the same template. Hot phase ~1–3 weeks, then decay: elsewhere557's views per post fell 2.03M → 154K as output rose. [L+C]
11. **Model** (`research/success-model.md`): can rank "beats the week median" (AUC 0.70) and 100K+ (0.69). Can't predict 1M+ (0.51). No account-level odds: there are no failed accounts in the data. [C]

## 3. Recommendation now: change the recipe, then test it
Single-variable tests need dozens of posts each at ~700 views, so it's too slow. Run the likely levers together as a new baseline for the next ~10 posts, compare them with the old 39, then remove levers one at a time if it works. [est]
- **Clip selection** (no editing): only clips that open on an upward reveal with the payoff in the first second, 8–11 s long, bright enough to read at 540p (no big black areas).
- **Sound:** October proven list (`research/data/proven_sounds.csv`): oscncs 18.8×, yuji 8.7×, Ark Patrol "Let Go" 6.9×, 𝙈𝙃𝘾 6.9×, Ca.Lyrics 5.5×. Give each 2+ tries. Skip likely paid promos (CIGARETTES, gambling, "i'm tired", "farewell cruel world").
- **Upload:** TikTok Studio web, "Upload HD" on if offered, Content check lite PASS, post directly, 1–3 posts/day spaced hours apart, credit the creator.
- **Log every post** in log.csv: tiktok_link, 1 h and 24 h views/likes, shares, saves. Also % For You and % watched to end from Studio.
- **First milestone:** any post ≥10–15% likes/view (network flop range). [est]

## 4. Open conflicts / unknowns
- **Dark charm vs compression:** charm v3 wants a dark muted grade, but at 540p / 0.5 Mbps dark footage turns to mush. Pick brighter clips first. Grading is Vyx's call (see §5).
- **Was someplace505's hit batch self-filmed?** That label is a vidIQ AI guess. Local work suspects Douyin reposts (e.g. 可爱到爆炸). Unverified.
- **60 fps:** the model says 1.8× odds of 1M+, the levers analysis says no effect. Untested by us.
- **Which clips were the 4 posts of 21 Oct** (7/7/7/9 s, IDs in research/data/papercheques_videos.csv)? None matches p68–p72's lengths (8.6–13.3 s). Trimmed? Vyx to say. log.csv has links only up to p67.
- Does TikTok withhold 1080p from small accounts, or does quality follow engagement? Can't tell from outside data.

## 5. Waiting on Vyx
1. **Rule 1 scope:** is a format-only re-export (1080×1920 H.264, same picture) OK? Is a light exposure lift or denoise OK, or does it count as a filter? Until you answer: no changes to the picture.
2. **Rule 3 extension** (proposed 21 Oct): scripts may read our post list, but never load or download our video pages or files. Confirm.
3. Fill the tiktok_link for each posted p-number (from the Studio post list).

## 6. Pipeline
- Next file number: **p73**.
- Ready (permission yes, precheck OK, still need Content check lite): p65 night snowfall car park, p66 qingdao blue hour towers (2.1 Mbps, ask for the original), p68–p72 (unless they were the 21 Oct posts).
- Hold: p61 (TikTok collision check not done). Never: p54, p63 (re-uploaded shoots), p55–p57 (baked signatures).
- Permission yes, not downloaded: 鱼丸三三. Permission not confirmed: 梁同学, 雾必野.
- Seasonal lead: Yunnan 冬樱花 (winter cherry), usually mid-Nov to Dec [est, verify].
- Score so far: the snow posts flopped (p48 699, p49 332, p64 681, p67 155). p60 (dusk window, fast early likes) also ended at 712 views and 4.1% likes, so no theme has beaten ~700 yet. That fits "engagement, not theme". [C data]

## 7. Latest agent reports
None yet. Each agent overwrites its own file: `reports/scout.md`, `reports/gate.md`, `reports/rivals.md`, `reports/self.md`.
