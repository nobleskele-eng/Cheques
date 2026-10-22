# MASTER: @papercheques current state
Updated 2026-10-22 11:42 UTC, cloud (v7b: elm). Cap 8,000 bytes. Overwrite stale lines; old versions are in git history. Tags: [L] local work, [C] cloud research, [V] Vyx, [est] estimate.

## 1. Where we are
- ~55 followers. 40 public posts, 3–22 Oct (cloud self pull OK 22 Oct 11:07 UTC). Every post gets ~700 views (median 712, most 450–1,100): TikTok tests each one, but the test audience doesn't react. Best: 2,207 (10 Oct). [C]
- Our medians: 5.2% likes/view, 0.00% shares, 0.28% saves; like rate falling 6.3% (3–10 Oct) → 5.1% (11–16) → 4.2% (18–21). Network flops (<10K views): 8–11% likes, 0.6–1.1% shares. Breakouts (100K+): 21–25% likes, 2–4% shares (lifetime rates; direction only). [C] [L csv]
- Sourcing is good enough [V]: permissioned Douyin clips, and big accounts got millions from clips Vyx posted first. **Bottleneck = test-audience engagement.**
- FYP "unoriginal" flags: p53, p58, p59, p62. Account in good standing [V 19 Oct]. Raw reposts resumed, only after a Content check lite PASS.

## 2. What we know (strongest first)
1. **Content check lite** (TikTok Studio web upload) predicts flags: PASS → no flag 3/3 (p60, p64, p67). ERROR → p58 flagged, p54 never posted. n=5. Also rejected at lite: p65, p69. p74 (3-day-old source) passed almost instantly; p73 (12 days old, 8.9K shares) stuck = likely ERROR [V]. Check time may be a signal. [L]
2. **Sound:** another account's sound mostly beats official tracks (1.24–1.53× vs 0.36–0.80× same-week views), but official "Let Go" (Ark Patrol) is elsewhere557's live hit: 11.6× over 6 uses; 4 posts 17–20 Oct: 182K–5.3M. 37/39 of ours use an account's sound, only 1 of 22 "proven" ones; n=3–8 per sound. [C]
3. **Served quality:** 0/39 of ours have a 1080p version (best ~533 kbps, 540–720p); the network gets 1080p on 81–99% of posts, flops included. Brightness alone doesn't track views: p60 (YAVG 42) 712, p64 (103) 681, p67 (104) 155. [C] [L gate]
4. **Openings:** all top 5 of the network's hit batch open on an upward reveal (tilt up from the ground or a railing). The 3 of ours checked are mostly static. n=8+3. [C]
5. **Length and cuts:** 23/39 of ours run 6–7 s; network hits 7–11 s, and 11–14 s+ did 1.1–2.0× (small n). [C] **Our clips get cut short between file and post:** 9 of 12 mapped posts since 5 Oct ended 6–9 s, 1.3–9.5 s shorter (median −3.0 s), AE edits and raw alike. Network lengths match their files. Full vs cut: no difference yet (certain n=3 vs 9: median 798 vs 709). [L ffprobe + csv]
6. **Volume:** views per post drop past ~3/day (someplace505) or ~6/day (elsewhere557). [C]
7. **Posting mode:** scheduled median 353 vs direct 716 (n=3 vs 36; 12 h ahead → 31 views). Posted <10 min apart (n=4): 758, 912, 461, 159; 42 min–2 h apart: ~700 each. Post directly, 40+ min apart. [L csv + decode]
8. **Hour (confounded):** 23:00–02:30 UTC (19:00–22:30 EDT) n=10: median 792, none <650, holds the top 4. 02:30–05:00 UTC n=19: median 687, 7 of 8 posts <600, but 6 of those 7 were scheduled or stacked; 3 of the top 4 were one Friday. A test, not a rule. [L csv]
9. **The network is a business** (sound promo, €54.99 course). kadzoo55871 + elsewhere557 (+ anywhere557) = one operator; someplace505 likely separate. **New: rvf5567** (22 Oct) is very likely theirs: same blank name, language "fr", house sound "lovers rock"; first posts 310–859 views, 15% likes. Hot phase ~1–3 weeks, then decay: elsewhere557 weekly median 102K (wk 28 Sep) → 20K (wk 19 Oct, partial). [C]
10. **Model** (`research/success-model.md`): ranks 100K+ (AUC 0.69), not 1M+ (0.51). [C]

## 3. Recommendation now: change the recipe, then test it
Single-variable tests need dozens of posts at ~700 views, so run the likely levers together as a new baseline for ~10 posts, compare with the old 39, then remove levers one at a time if it works. [est]
- **Next posts = p73–p75** (approved 22 Oct, new DM allows colour and trims). Every inbox clip p65–p72 has already been posted or tested [V 22 Oct]. The p69/p72 edits are spare: p69 was tested and rejected on 20 Oct. These are the first new-recipe posts; record recipe fields in log.csv when posted.
- **Check length before Post:** the TikTok editor preview must show the file's full length. If it's shorter, stop and note the step.
- **Clip selection:** upward reveal, payoff in the first second, 8–13 s. **Post at full length.**
- **Edit for 540p**: lift exposure, denoise, export 1080×1920 H.264 at a high bitrate, muted palette. Save as `pNN … edit.mp4`.
- **Sound** (`research/data/proven_sounds.csv`): oscncs 18.8×, Let Go 11.6×, Cherry 10.4×, yuji 8.7×. Give each 2+ tries. Skip likely paid promos (CIGARETTES, gambling).
- **Upload:** TikTok Studio web as drafts, "Upload HD" if offered, Content check lite must PASS. Post directly, never scheduled, 1–3/day, 40+ min apart. Credit the creator by the 抖音号 on their profile.
- **Log every post** in log.csv: tiktok_link, 1 h and 24 h views/likes, shares, saves, % For You, % watched to end.
- **First milestone:** any post ≥10–15% likes/view (network flop range). [est]

## 4. Open conflicts / unknowns
- **Dark charm vs compression:** charm v3 wants a dark muted grade, but at 540p / 0.5 Mbps dark footage turns to mush. Lifted-but-muted edits (e.g. YAVG 93→104) are untested on a live post. [L]
- **rvf5567 DM'd us 22 Oct:** "all your videos are reposted". True by design (permissioned reposts); likely a course-funnel opener [est]. Reply: ask which clips. Source doubts: p62 (_青), Hana. [V]
- **@.1elm:** DM'd on Discord 22 Oct [V]. 757 posts since Dec 2023, ~1/day, 11 s, 1080p 79%; Oct median 140K, 24% likes; first months ~1.3K. [C]
- **Our log is behind Vyx:** p65, p69 + one unknown rejected at lite; the 4 posts of 20–21 Oct (EDT 22:42, 23:24, 00:06, 02:00 scheduled) not mapped yet (§5.3). [V][L]

## 5. Waiting on Vyx
1. **p74:** which file went up (edit or original)? Did the editor preview show 9 s or 8 s?
2. **Who shortens clips:** you, or TikTok when the sound is added? Post at full length either way.
3. tiktok_links for the 20–21 Oct posts (§4). Third lite reject: unknown (not p66–p68).
4. Download p75/p76 (one load each, or SaveTik). Still open: 雾必野 permission; 鱼丸三三 download.
5. Cloud self pull: first test is the Sat 24 Oct run.
6. rvf5567 DM: which clips did they name?

## 6. Pipeline
- Next file number: **p77**.
- **New recipe (permission yes 22 Oct [V]):**
  - **POSTED p74** (梁同学 train door, 9.3 s, YAVG 45→53 edit) 21 Oct 23:25 EDT with "Let Go": new-recipe post 1. At 7.7 h: 703 views, **2.3% likes** (bar 5%), 1 share, 1 save; 8 s on TikTok (~1 s cut); served 540p h264 336 kbps, no 1080p. Failed. [C pull]
  - p73 (balcony tilt-up, 11.2 s) stuck at lite → likely blocked. Vyx downloaded both via SaveTik (1080p, 1.3–1.9 Mbps).
  - **Not downloaded** (our Douyin pane was bounced 22 Oct): p75 谢景行 7693926803313088960 (7.7 s Dali lane, shares 33% of likes) and p76 韬 7697564623889337435 (8.0 s HK rain, dark).
- **Used up:** p65–p72 [V]. p65 and p69 were rejected at lite; the rest were posted (except one unclear). The p69/p72 edits in the inbox are spare.
- HOLD p61 (TikTok collision check not done). Never: p54, p63 (re-uploaded shoots), p55–p57 (baked signatures).
- Permission yes, not downloaded: 鱼丸三三. Not confirmed: 雾必野.
- Seasonal lead: Yunnan 冬樱花, mid-Nov to Dec [est].
- Score so far: snow posts 0 for 4 (p48 699, p49 332, p64 681, p67 155); p60 712. No theme has beaten ~700. [C data]

## 7. Latest agent reports
- `reports/rivals.md` 22 Oct: "Let Go" live hit; decay continues.
- `reports/self.md` 22 Oct (local, 21 Oct csv): 9 of 12 clips cut; scheduled vs direct; hour split.
- `reports/scout.md` 22 Oct: 3 DM picks; Douyin throttled at load 11 (use rec lists and profiles on such days).
- `reports/gate.md` 22 Oct: p65–p72 checks; the edit recipe.
- `reports/watch.md` (every 6 h until 5 Nov): rvf5567 live tracker.
