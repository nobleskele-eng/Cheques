# @papercheques Diagnosis: Why the Test Audience Isn't Engaging

**Data:** pulled 2026-10-21. 39 public videos posted 2026-10-03 → 10-21.
**Files:**
- `research/data/papercheques_videos.csv`, `research/data/papercheques_encoding.csv`, `research/data/papercheques_sounds.csv`: the same format as the network accounts, so the model can use them.
- `research/data/proven_sounds.csv`: the network's reused sounds, ranked.

---

## 0. Answer

1. **TikTok *is* testing your videos.** Every post gets a steady **~700 views** (median 712; most between 450 and 1,100).
2. **That audience barely reacts.** You get **5.2% likes per view, 0.0% shares, 0.3% saves**. That's below even the network accounts' *flops*.
3. **Duplicate footage isn't the cause.** None of your 39 thumbnails is close to any of their 748.
4. **Sound choice isn't the whole cause either.** Sounds that worked for the network still got you ~700 views and 3–8% likes.
5. **What's left, in order of likelihood:**
   - **(a) What the test audience sees:** TikTok serves your videos at **540–720p and 0.1–0.6 Mbps**. Your footage is very dark, and at that bitrate dark footage turns to blocky mush.
   - **(b) Weak openings:** your videos are mostly static. The network's top hits all open on an upward reveal.
   - **(c) Short clips:** most of yours are 6–7 s, against 7–11 s for the network's hits.
6. **(a) is only partly in your control.** TikTok seems to make high-quality versions only once a video or account has traction (§2). What you *can* control is what survives heavy compression.

---

## 1. Your numbers against the benchmarks

| | @papercheques (median) | Network flops (<10K views) | Network breakouts (100K+) |
|---|---|---|---|
| Views per post | 712 | n/a | n/a |
| Likes per view | **5.2%** (best 8.7%) | 8–11% | 21–25% |
| Shares per view | **0.00%** | 0.6–1.1% | 2–4% |
| Saves per view | **0.28%** | ~1% | 2–3% |
| Length | 6–7 s on 23 of 39 videos | n/a | Hit batch: 7–11 s |

**Benchmark caveat:** the network figures are lifetime rates from accounts with 200K–380K followers. I have no reliable benchmark for a 55-follower account's first-hour audience. Use these as a direction, not a target you'll hit exactly.

**One video got 31 views.** That's far below your usual 450+. It may have been held back from the For You feed, so check TikTok Studio for a notice on it.

## 2. What the test audience actually sees

| | @papercheques | Network accounts |
|---|---|---|
| Videos with a 1080p version | **0 of 39** | 75–99% (including their flops); 100% of their posts from the last 3 days |
| Versions per video | 1 on 25 videos (just "lowest_540") | Usually 5 |
| Best version's bitrate (median) | **533 kbps** (files measured: 126, 298, 590 kbps) | ~1,800–2,000 kbps |
| TikTok's source-quality score for your upload | **74.4** | 75.9–77.4 |

**Reading:**
- Your *uploads* score about the same quality as theirs. TikTok just never built the high-quality versions for yours.
- That's consistent with your theory that quality is held back for low-traction accounts or videos. I can't prove it's the cause rather than the effect.
- **Your controllable lever:** make footage that still reads at ~0.5 Mbps and 540p:
  - lift the exposure;
  - avoid large black areas (one sampled clip is about half black window frame);
  - denoise before export;
  - make sure TikTok's own **"Upload HD"** option is on when posting.

## 3. Sounds

- **37 of your 39 videos** use another account's sound, which is the right category. 1 uses an official library track; 1 uses your own audio.
- **15 of them** are sounds the network also used. The ones the network reused 3+ times went a median of **1.6×** its typical video there. On your account they still got ~700 views, so **sound alone isn't the bottleneck**.
- **You've used only 1 of the 22 "proven" sounds:** network sounds with 3+ uses, ≥2× the week median, and ≥60% beating it.
- **Avoid the network's likely paid promos.** These are official tracks they reuse heavily *despite* below-median results: "CIGARETTES" ×36 (0.81×), "gambling" ×17 (0.91×), "farewell cruel world…" ×10 (0.68×), "i'm tired" ×8 (0.36×). The `likely_paid_promo` column in `proven_sounds.csv` flags these. It's a heuristic, not verified.

**Proven sounds the network was still using in October** (from `proven_sounds.csv`):

| Sound | Author | Network uses (Oct) | Median vs week | Beat rate | Link |
|---|---|---|---|---|---|
| original sound | oscncs | 3 (3) | 18.8× | 67% | https://www.tiktok.com/music/x-7692131847752436494 |
| original sound - yuji | yuji | 5 (1) | 8.7× | 80% | https://www.tiktok.com/music/x-7687561451339516693 |
| Let Go | Ark Patrol (official) | 6 (6) | 6.9× | 83% | https://www.tiktok.com/music/x-7385586638095321105 |
| original sound | 𝙈𝙃𝘾 | 3 (1) | 6.9× | 100% | https://www.tiktok.com/music/x-7679868563990383382 |
| original sound | Ca.Lyrics 🎧 | 4 (1) | 5.5× | 100% | https://www.tiktok.com/music/x-7603885847720594206 |
| original sound | Cherry | 5 (5) | 4.6× | 60% | https://www.tiktok.com/music/x-7632470897454041874 |
| original sound | ʚminachiiiɞ | 8 (8) | 4.5× | 62% | https://www.tiktok.com/music/x-7600721158866619156 |
| original sound | sayura | 3 (2) | 2.7× | 67% | https://www.tiktok.com/music/x-7441550204486306616 |
| original sound | shinobi | 9 (6) | 2.4× | 67% | https://www.tiktok.com/music/x-7678789856931351310 |
| New Computers | Girlfriends (official) | 3 (3) | 2.3× | 67% | https://www.tiktok.com/music/x-7554861805249054721 |

Each sound's effect is measured on only 3–9 videos, so the rankings are noisy.

## 4. Footage and openings (3 videos checked frame by frame)

| Video | Views | Opening | Notes |
|---|---|---|---|
| Night waterfront, LED skyline (China) | 2,207 (your best) | Walks from the pavement up to the skyline: **a reveal** | On-format |
| Rainy steps under an elevated train | 1,097 | Static | Only 6 s |
| Shanghai skyline through a window at dusk | ~700 | Static | About half the frame is black window frame; served at **126 kbps** |

That's 3 videos, so it's suggestive only. But it lines up with the network's hit batch, where all top-5 videos opened with an upward reveal.

## 5. What to change, and how to test it

1. **Every video opens with a reveal:** start on the ground or something close, then tilt up to the view within the first second.
2. **Make it survive compression:**
   - brighter exposure, no big black areas;
   - denoise before export;
   - "Upload HD" on;
   - 1080×1920.
3. **Run 8–11 s instead of 6–7 s.**
4. **Use the proven October sounds above.** Give each 2+ tries (@someplace505's breakout sound failed on its first try). Skip the likely promos.
5. **Change one thing at a time, and keep a log.** For each post, record 24-hour views, likes per view, shares per view, % from the For You feed, and % watched to the end.

**First milestone** *(rough estimate, not a measured threshold)*: get any single video to roughly **10–15% likes per view**. That's the network's flop range, and it's where your test audience starts reacting.

## 6. Limits

- **Small samples:** 39 videos on your account, 3 checked frame by frame, and sound effects measured on 3–9 network videos each.
- **The quality question is open:** whether TikTok withholds quality from small accounts, or quality simply follows engagement, can't be told apart from outside data.
- **No small-account benchmark:** what "good" looks like for a 55-follower account's test audience isn't public.
