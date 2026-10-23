# Replication Levers and Encoding (Bitrate) Analysis

**Data:** TikTok's creator video list plus actual video files, pulled 2026-10-21.
**Coverage:** @someplace505 176/176 videos, @elsewhere557 572/581. 22 video files were downloaded, measured with ffprobe and then deleted.
**Related:** [growth regression](tiktok-growth-regression.md) · [content-style analysis](tiktok-someplace505-elsewhere557-analysis.md) · [plain summary](reliability-plain-summary.md)

> **Everything here is correlation, from two accounts that already succeeded.** It shows what went with more views on *these* accounts. It doesn't prove what causes views, and it won't guarantee results on a new account.

> **Correction (2026-10-21).** An earlier version of this doc said "bake the audio into the video file" and credited original-quality uploads with 1.44–7.23×. Both were wrong. They came from grouping sounds by *title* ("original sound" vs a song name).
>
> Sound IDs carry their creation time, and they show that both accounts pick their sound in TikTok's upload screen on **88% (@someplace505) and 99.7% (@elsewhere557)** of videos. The corrected analysis is §2 "Audio" and the updated items 1 and 4 below.

---

## 0. Answer: the best evidence-based way to replicate

Ranked by strength of evidence.

**Strong (consistent on both accounts)**
1. **Add the sound in TikTok's upload screen, and pick another account's uploaded version of the song** rather than the official library track. These user versions are often sped-up, slowed or edited cuts, and TikTok labels them "original sound".
   - Same-week relative views:
     - another account's sound: **1.24×** (@elsewhere557) and **1.53×** (@someplace505);
     - official library track: **0.36×** and **0.80×**.
   - *(Relative views = a video's views ÷ the account's median for that week, so 1.0× is an average week.)*
   - The sounds they pick had been created a median of **98 days** (@elsewhere557) and **51 days** (@someplace505) earlier. Both accounts draw from the same uploaders: "lia", "imar" and "by your side" appear on both.
2. **Upload at full 1080×1920 or above.** @elsewhere557's few uploads without a 1080p tier did **0.21×** (22 videos, only 18% beat their week's median).
3. **Keep daily volume moderate.** Views per post drop beyond ~3 posts/day (@someplace505) and ~6/day (@elsewhere557).
   - On @elsewhere557, days with 2–3 posts did **2.43×** per post, vs **~0.9×** on days with 7+.
   - Its first post of the day did **1.66×**.
   - *Not shown:* whether *total* daily views fall with more posts. More posts are still more chances at a hit.

**Moderate (one account only)**

4. **Own-audio uploads (one batch on @someplace505).** On 22 videos, @someplace505 uploaded its own audio, creating a new sound titled "original sound - ￴ ￴". 19 of those 22 were also served as the original file, likely via the third-party uploader (§1.3).
   - Those 19 did **10.27×** (95% beat their week's median).
   - The quality bypass *on its own* showed no benefit: original-file uploads that used another account's sound did **0.81×** (n=17), worse than re-encoded uploads with the same kind of sound (1.68×).
   - So the hits are a specific batch of own-audio uploads. §2.6 covers 8 of them:
     - all self-filmed China/Hong Kong travel POV, one take, 7–11 s;
     - the top 5 all open with an upward reveal;
     - the audio is a mix of anime dialogue, ambient/synth and slowed songs.
   - @elsewhere557 never does this.
5. **Slightly longer clips:** 11–14 s+ did 1.13–1.98× on both accounts, but sample sizes are small.

**No measurable effect (skip)**
- **60 fps vs 30 fps:** @elsewhere557 did 1.00× at ~60 fps vs 1.15× at ~30 fps on beating the week median.
  - ⚠ **Conflicting signal:** the [success model](success-model.md) finds 60 fps uploads had **1.8× the odds of reaching 1M+**. But the model can't predict 1M+ hits on held-out data, so that may be noise or a side effect of what was filmed.
  - **Don't switch frame rate on this evidence alone. Test both.**
- **Loudness, and TikTok's own quality scores:** no meaningful link to views.
  - On @elsewhere557 the correlations are −0.04 to −0.01.
  - @someplace505's loudness correlation is −0.15, and its quality scores are missing for most videos, so those can't be tested properly.
- **Posting time of day:** the two accounts disagree, so there's no reliable signal.

**Untestable from this data, but both accounts had it**
- An older account that was renamed and relaunched (created 157 / 638 days before its first visible video).
- A sibling network of near-identical accounts posting shared sounds.
- The timing of their August 2026 takeoff.

**The format baseline** (from the content-style analysis):
- a 7–13 s single first-person shot;
- no on-screen text, no face, empty caption;
- moody real-world footage (rain, night, Japan-coded).

### Where your video-source research fits

I haven't seen it yet. Footage sourcing settles three things the data can't:
- **Originality risk.** Self-shot, licensed stock, or other creators' clips? Reposting others' footage risks takedowns and reduced reach on the For You feed.
- **Cost per video.** This decides whether 3–6 posts a day is sustainable.
- **The "foina" watermark** on one @elsewhere557 clip: is it the account's own mark or a source creator's?

Share it and I'll fold it into this ranking.

### How to run a replication properly *(rough estimate, reasoning from the data, not a measured base rate)*

On these accounts about 1 in 6 videos passed 1M views, so results are lottery-like. Judge any change only after roughly **60–120 posts** (3–6 a day for 2–3 weeks), using the same relative-views measure, not single videos.

---

## 1. Bitrate and encoding

### 1.1 What TikTok serves (API data, all videos)

| | @someplace505 (176) | @elsewhere557 (572) |
|---|---|---|
| Served as the **original upload, not re-encoded** | **39 videos (22%)**, median **~27 Mbps** | 0 |
| Re-encoded videos with a 1080×1920 tier | Varies; the tier list returned is inconsistent | 546 (95%) |
| Uploaded at ~60 fps (59–60 fps tier exists) | 8 of the re-encoded videos, **plus all 7 originals sampled in §1.2** | **405 (71%)** |
| Best re-encoded tier, median bitrate | 1,824 kbps | 1,776 kbps (10th–90th percentile: 931–3,430) |
| Codecs of re-encoded tiers | H.264 and H.265 (HEVC) | Mostly HEVC; H.264 for fallback tiers |
| Audio | 32–146 kbps AAC (originals); ~65 kbps HE-AAC (re-encoded) | 65–98 kbps HE-AAC |
| Loudness (TikTok's reading, likely LUFS), median | −13.9 (10th–90th percentile: −22.4 to −9.0) | −16.6 (−24.7 to −13.9) |
| TikTok source-quality score, median | 77.4 (only 47 videos have one) | 75.9 |

### 1.2 Measured files (ffprobe on downloaded videos)

| Account | Views | What TikTok served | Video | Video bitrate | Audio | Length |
|---|---|---|---|---|---|---|
| @someplace505 | 20,600,000 | Original file | H.264 1080×1920 **60 fps** | **34,783 kbps** | HE-AAC 32 kbps | 8.2 s |
| @someplace505 | 8,600,000 | 480p tier (only tier offered) | HEVC 480×854 30 fps | 308 kbps | HE-AACv2 25 kbps | 8.0 s |
| @someplace505 | 6,200,000 | Original file | H.264 1080×1920 60 fps | 21,053 kbps | AAC-LC 128 kbps | 8.6 s |
| @someplace505 | 2,200,000 | Original file | H.264 1080×1920 60 fps | 29,969 kbps | HE-AACv2 32 kbps | 10.4 s |
| @someplace505 | 164,200 | Original file | H.264 **2160×3840 (4K)** 60 fps | 30,348 kbps | HE-AACv2 32 kbps | 8.0 s |
| @someplace505 | 20,300 | 720p tier | HEVC 720×1280 30 fps | 1,112 kbps | HE-AACv2 55 kbps | 7.7 s |
| @someplace505 | 17,100 | 1080p tier | H.264 **1920×1080 (landscape)** 30 fps | 5,598 kbps | HE-AACv2 65 kbps | 8.7 s |
| @someplace505 | 14,700 | Original file | H.264 1080×1920 60 fps | 26,944 kbps | AAC-LC 146 kbps | 11.2 s |
| @someplace505 | 14,000 | Original file | H.264 1080×1920 60 fps | 33,511 kbps | AAC-LC 101 kbps | 11.3 s |
| @someplace505 | 4,387 | Original file (first-ever video) | H.264 1080×1920 60 fps | 28,045 kbps | AAC-LC 131 kbps | 11.2 s |
| @someplace505 | 4,054 | 1080p tier | H.264 1080×1920 30 fps | 4,565 kbps | HE-AACv2 66 kbps | 6.8 s |
| @someplace505 | 1,669 | 1080p tier | H.264 1080×1920 30 fps | 4,586 kbps | HE-AACv2 65 kbps | 8.1 s |
| @elsewhere557 | 17,700,000 | 1080p tier | HEVC 1080×1920 60 fps | 5,114 kbps | HE-AAC 97 kbps | 13.2 s |
| @elsewhere557 | 16,500,000 | 1080p tier | HEVC 1080×1920 59.94 fps | 2,995 kbps | HE-AAC 98 kbps | 7.4 s |
| @elsewhere557 | 9,700,000 | 1080p tier | HEVC 1080×1920 29.97 fps | 1,805 kbps | HE-AAC 98 kbps | 7.0 s |
| @elsewhere557 | 2,000,000 | 1080p tier | HEVC 1080×1920 60 fps | 3,275 kbps | HE-AACv2 65 kbps | 7.9 s |
| @elsewhere557 | 1,200,000 | 1080p tier | HEVC 1080×1920 59 fps | 1,828 kbps | HE-AACv2 65 kbps | 9.2 s |
| @elsewhere557 | 439,400 | 1080p tier | HEVC 1080×1920 59.94 fps | 1,289 kbps | HE-AACv2 65 kbps | 8.8 s |
| @elsewhere557 | 53,300 | 1080p tier | HEVC 1080×1920 60 fps | 549 kbps | HE-AACv2 65 kbps | 9.2 s |
| @elsewhere557 | 27,400 | 1080p tier | HEVC 1080×1920 59.94 fps | 2,585 kbps | HE-AACv2 66 kbps | 6.8 s |
| @elsewhere557 | 2,702 | 720p tier | HEVC 720×1280 30 fps | 675 kbps | HE-AACv2 66 kbps | 7.2 s |
| @elsewhere557 | 2,165 | 720p tier | HEVC 720×1280 30 fps | 437 kbps | HE-AACv2 65 kbps | 9.6 s |

**Sample:** the top 3, bottom 2 and 5 random videos per account, plus 2 extra originals for @someplace505.

**Limit:** for re-encoded videos, this is the best tier TikTok offered *this client*. Higher tiers may exist. For example, the 8.6M-view @someplace505 video was only offered at 480p here.

### 1.3 What it means

- **@someplace505's export settings:** its originals show it exports **1080×1920 (sometimes 4K) at 60 fps, H.264, about 21–35 Mbps**. That's roughly 10× what TikTok normally serves, and it matches a high-quality editor export.
- **TikTok skipping the re-encode is unusual.** One of @someplace505's videos, since deleted, carried the caption "HD BY Rein — Upload Method by reinpengenhd". That refers to a third-party uploader advertised for 1080p/60 fps uploads. **[Inference]** That tool is the likely reason these files are served untouched.
  - **Risk:** third-party upload tools typically need access to your TikTok session, which is an account-security and terms-of-service risk. I can't verify the tool is safe.
  - **Safer first test:** TikTok's own "Upload HD" setting.
- **@elsewhere557's export settings:** it uses the normal upload path, exporting 1080×1920, mostly at 60 fps. TikTok re-encodes everything to **0.5–5 Mbps HEVC**. The bitrate a viewer sees varies with how complex the scene is (rain and motion cost more bits), not with how well the video did.
- **Delivered bitrate doesn't predict views** on @elsewhere557 (correlation +0.03). What mattered there was *not* uploading below 1080p.

---

## 2. What went with more views (same-week relative views)

**Method:**
- Only the active period, from 2026-08-24, is used.
- Each video's views are divided by the median views of that account's videos posted the same week. This removes the takeoff and decay trends.
- Groups need at least 8 videos (5 for upload quality).

#### Audio: where each video's sound came from

Each sound ID encodes when the sound was created:
- A sound created within an hour of the video, by the same account, came in with the upload.
- Anything older, or by another account, was picked in TikTok's upload screen.

| Sound origin | @someplace505 | @elsewhere557 |
|---|---|---|
| Picked in-app: another account's sound | 50 videos, **1.53×** (n=50, 60% beat week median) | 461 videos, **1.24×** (n=370, 55%) |
| Picked in-app: official library track | 104 videos, 0.80× (n=104, 36%) | 109 videos, **0.36×** (n=107, 30%) |
| New sound created by its own upload | 22 videos, **7.28×** (n=21, 90%) | 1 video (n=1, 0.06×) |
| Re-used its own earlier sound | 0 | 1 video (0.56×) |

*Counts are all videos; relative views use the active period only.*

- **Commercial matches:** TikTok matched the audio to a commercial song on 130/176 (@someplace505) and 260/572 (@elsewhere557) videos. Many "another account's sound" uploads are re-uploads of real songs.
- **Shared sounds:** 52 (@someplace505) and 123 (@elsewhere557) videos use a sound ID that the other account also used.
- **Hint of a previous identity:** @someplace505's very first video (2026-06-16) uses a sound titled "suara asli - Spax" (Indonesian for "original sound"). That suggests the account went by "Spax" before its 2026-08-27 rename.

#### Upload quality × sound origin (@someplace505)

| | Own new sound | Another account's sound | Official library track |
|---|---|---|---|
| Original file served | **10.27×** (n=19, 95%) | 0.81× (n=17, 47%) | 1.19× (n=3) |
| Re-encoded | 1.01× (n=2) | 1.68× (n=33, 67%) | 0.80× (n=101, 35%) |

**Reading:** the original-file upload doesn't help by itself (0.81× vs 1.68× with the same kind of sound). The effect is concentrated in the 19 own-sound uploads, and the two can't be separated.

On @elsewhere557, which is all re-encoded, another account's sound did 1.24× vs 0.36× for official tracks.

#### Volume per day

| Posts that day | @someplace505 | @elsewhere557 |
|---|---|---|
| 2–3 | **1.16×** (n=69) | **2.43×** (n=18) |
| 4–6 | 0.90× (n=96) | 1.20× (n=84) |
| 7–10 | n/a | 0.90× (n=170) |
| 11+ | n/a | 0.92× (n=206) |
| Typical posts per day (median / max) | 3 / 7 | 8 / 25 |

| Order within the day | @someplace505 | @elsewhere557 |
|---|---|---|
| 1st post | 0.91× | **1.66×** (n=59, 69%) |
| 2nd–3rd | 1.05× | 1.00× |
| 4th–6th | 0.89× | 0.72× |
| 7th+ | n/a | 0.98× |

#### Length and frame rate

| | @someplace505 | @elsewhere557 |
|---|---|---|
| ≤6 s | 0.88× (n=8) | 0.88× (n=56) |
| 7–8 s | 1.00× (n=87) | 1.00× (n=237) |
| 9–10 s | 1.02× (n=57) | 0.78× (n=101) |
| 11–13 s | 1.13× (n=20) | 1.23× (n=59) |
| 14 s+ | n/a | **1.98×** (n=26) |
| Re-encoded at ~60 fps vs ~30 fps (1080p tier) | 1.00× (n=7) vs 0.73× (n=39) | 1.00× (n=340) vs 1.15× (n=117) |
| Below 1080p tier | 0.92× (n=90) | **0.21×** (n=22) |

**Posting time (UTC):** the best block was 04–07 UTC on @someplace505 (1.21×) and 12–15 UTC on @elsewhere557 (1.62×). The two accounts disagree, so there's no usable signal.

---

## 2.5 Does TikTok restrict quality for low-view posts? (tested 2026-10-21)

**Not in this data.**

| Views | @elsewhere557: has a 1080p tier | @elsewhere557: best-tier bitrate (median) | @someplace505: has a 1080p tier |
|---|---|---|---|
| <10K | 81% (44/54) | 1,958 kbps | 75% (12/16) |
| 10K–100K | 96% (225/235) | 2,012 kbps | 34% (32/93) |
| 100K–1M | 99% (186/188) | 1,983 kbps | 9% (1/11) |
| 1M+ | 99% (94/95) | 2,006 kbps | 12% (2/17) |

- **@elsewhere557:**
  - Best-tier bitrate is flat across every view level.
  - All 20 videos posted in the last 3 days already had a 1080p tier (median 32K views).
  - So a missing 1080p tier is more likely a property of that upload than a penalty for low views.
- **@someplace505 shows the reverse:** its *popular* videos were offered fewer and lower tiers. Its 8.6M-view video was offered only at 480p. That might be TikTok saving bandwidth on heavily-watched videos, or it may depend on the device requesting it.
- **No re-encoded tier above 1080×1920 exists in any of the 748 videos.** A 4K upload is only ever *seen* in 4K when TikTok serves the original file (@someplace505's case).
- **60 fps gets half the bits per frame.** TikTok gives 1080p HEVC tiers about the same bitrate at both frame rates: a median of 1,764 kbps at ~30 fps vs 1,836 kbps at ~60 fps. That's **64 vs 31 kb per frame**.
  - 60 fps also showed no view benefit: 1.00× vs 1.15× (§2).
  - So for slow mood footage, a 30 fps export should look cleaner after re-encoding.
  - **But** see the frame-rate warning in §0: the success model links 60 fps with more 1M+ hits. Cleaner frames and more views may pull in opposite directions, so test both.

**Limit:** this is what an anonymous web viewer was offered at one moment. The phone app, or the first few hours after posting, may behave differently.

## 2.6 Inside @someplace505's hit batch (8 of the 19 own-audio, original-file videos watched)

**Method:**
- vidIQ AI frame-by-frame breakdowns, 2026-10-21.
- Picked to span the batch's results: the top 5 by views, plus 3 lower ones.
- Song and dialogue identifications are vidIQ's and unverified.

| Views | Location (from signage and landmarks) | Footage | Opening | Audio | Length |
|---|---|---|---|---|---|
| 20,600,000 | Jiuzhaigou Valley, Sichuan, China | Turquoise lake from a boardwalk, daytime | Tilt up from the water to the lake and mountains | *Attack on Titan* dialogue, Japanese ("beyond the walls is the ocean… beyond the ocean is freedom"), plus animated Japanese text of the line. **The only video with on-screen text.** | 8 s |
| 6,200,000 | Central, Hong Kong | Night skyline (Bank of China Tower) from a footbridge | Fast whip-pan up from the street | Instrumental synth plus a whoosh effect | 8.8 s |
| 2,500,000 | Changsha, Hunan, China | Rainy night street under an umbrella | Tilt up from wet pavement | English indie song ("And she cried… over nothing…") | 11 s |
| 2,200,000 | Jiuzhaigou Valley, China | Turquoise lake, autumn leaves | Tilt up from the deck | *Attack on Titan* dialogue, Japanese ("this is… freedom") | 10 s |
| 2,000,000 | Victoria Harbour, Hong Kong | Stormy harbour at night, heavy blue grade | Tilt up from the railing | Storm ambience plus a synth bed, no vocals | 7 s |
| 250,800 | Unnamed Chinese city | Rainy street seen through a wet window, from above | Static | English song with the same lyric as the 2.5M video | 9 s |
| 58,700 | Chongqing, China | Rooftop skywalk over the night skyline | Tilt up from the feet | Slowed + reverb English pop | 10 s |
| 39,400 | Hong Kong | Rainy night street under an umbrella, two people in raincoats | Slight forward pan | Slowed + reverb English song (vidIQ: Don Toliver, "No Idea") | 7 s |

**What all 8 share:**
- **Self-filmed travel footage from China and Hong Kong.** Jiuzhaigou appears twice, Hong Kong three times, plus Changsha, Chongqing and one unnamed city. No watermarks, logos or other creators' marks.
  - This is *not* the Japan footage seen on @elsewhere557. The visual identity is "East Asian cityscape and nature", not Japan specifically.
- **One continuous shot, 7–11 s, no cuts.** No speed ramps, and none loop seamlessly.

**What separates the top 5 from the lower 3 (only 8 videos, so suggestive only):**
- **Opening move:** all 5 top videos open with an upward camera move (a tilt-up or whip-pan reveal). Only 1 of the 3 lower ones does.
- **Audio:** the top 5 lean on non-song audio (2× anime dialogue, 2× ambient/synth). The lower 3 are all slowed English songs.
  - *But* across the whole 19-video batch, the 5 clips TikTok matched to a commercial song did 15.7× the week median, vs 8.8× for the 14 with no match.
  - So "song vs no song" doesn't explain the batch's performance.
- **Theme matching:** the biggest hit pairs a "freedom / beyond the walls is the ocean" line with a reveal of a vast turquoise lake. The audio's meaning matches the picture.

**Limits:**
- The account's *other* videos (picked sounds, re-encoded) weren't watched, so I can't yet say how the batch's footage differs from them.
- vidIQ named two different songs ("Her" by eeryskies; "Romantic Homicide" by d4vd) for the same lyric in two videos. Treat song names as unverified.

## 2.7 Early engagement: benchmarks, and how @someplace505 got out of a cold start

**Limit:** test-pool (first-hours) data isn't public for other people's videos. Everything here uses lifetime totals, so it's a yardstick, not a measurement of the first hours.

**Engagement per view, by final views (medians):**

| Final views | @someplace505 likes / shares / saves | @elsewhere557 likes / shares / saves |
|---|---|---|
| <10K | 7.6% / 1.09% / 1.03% | 10.7% / 0.57% / 1.02% |
| 10K–100K | 13.0% / 1.35% / 1.68% | 18.4% / 1.26% / 1.99% |
| 100K–1M | 20.8% / 2.95% / 2.12% | 24.1% / 1.91% / 2.54% |
| 1M+ | 24.5% / 4.35% / 2.80% | 23.9% / 1.95% / 2.41% |

- **Rank correlation with total views** (post-takeoff), @someplace505 / @elsewhere557:
  - likes per view: **+0.74 / +0.71**
  - shares per view: +0.70 / +0.57
  - saves per view: +0.57 / +0.52
  - comments per view: −0.60 / −0.75
- **Rough yardstick (from established accounts):** breakouts sit at ~20–25% likes per view and ~2–4% shares per view. Flops sit at ~8–11% likes.
- **Reading it:** bigger reach usually *dilutes* engagement rates, yet here bigger videos have *higher* rates. That fits engagement driving distribution, which matches TikTok's own description that user interactions feed recommendations. But it's correlation.

**@someplace505's cold start.** It was renamed 2026-08-27; these are its first posts after that.

| Posted | Views | Likes / view | Sound |
|---|---|---|---|
| Aug 28 02:51 | 4,335 | 5.4% | "lovers rock" (another account's upload, created 1,279 days earlier) |
| Aug 28 16:01 | 4,387 | 4.2% | another account's sound |
| Aug 29 11:41 | 4,294 | 4.8% | official library track ("Self Aware") |
| Aug 30 02:19 | 6,418 | 6.6% | official library track ("nuts") |
| **Aug 30 06:11** | **972,200** | **24.0%** | **"lovers rock" again** |
| Aug 30 – Sep 10 | 0.4M–8.6M on most posts | 19–33% | "lovers rock" on 11 of its first 30 posts |

**What this shows:**
- The first four posts each stalled at ~4.3K views, with likes under 7%: the "test pool doesn't engage" stage.
- The breakout came on the **5th surviving post after the rename** (a 6th, posted on Aug 27, was later deleted), **within ~3 days, posting 2–3 a day**.
- It came on the **second** try of a long-established sound that had already failed once. The account then kept reusing that sound.
- The original-file upload method was on from the start of the relaunch, including during the stall, so it wasn't what broke the stall.

This is one account, so it's an example, not a rule.

## 3. Caveats

1. **Correlation, not cause.** For example, the operator may use the HD upload method and their own audio on footage they already think is strongest. Official library tracks may also include paid "sound promo" placements (both bios advertise sound promotion), chosen for payment rather than fit. That's a hypothesis, not verified.
2. **Survivorship.** Both accounts succeeded, and @elsewhere557 may have deleted around 59 underperforming videos (see the regression doc), which would flatter the survivors.
3. **Small groups.** Several cells have fewer than 30 videos. Treat effects under about 1.3× as noise.
4. **Partial tier lists.** The API and video pages return different tier lists for different clients, so the "best tier" for re-encoded videos is a lower bound.
5. **Original-file serving** is inferred from two things: no quality tiers listed, plus ~27 Mbps files being served. TikTok's own reason for not re-encoding them isn't documented.

## 4. Files

- `research/data/someplace505_encoding.csv`, `research/data/elsewhere557_encoding.csv`: one row per video. Columns: tier info, best-tier codec/resolution/fps/bitrate, TikTok quality scores, loudness, sound.
- `research/data/file_probe_sample.csv`: the 22 ffprobe measurements.
- `research/scripts/`:
  - `pull_tech.py`: re-pull with encoding fields.
  - `tech_summary.py`: encoding distributions and correlations.
  - `probe_sample.py`: download, probe, delete.
  - `levers.py`: the same-week relative-views tables.
  - `pull_music.py`, `sound_origin.py`: sound ID, creation time and author, plus the sound-origin tables.
- `research/data/someplace505_sounds.csv`, `research/data/elsewhere557_sounds.csv`: per-video sound ID, sound creation time, sound age when used, author, origin category, official-track flag and matched commercial song.

## 5. Lead from a peer creator (23 Oct, Vyx via Discord)
- "elmo" (another scenery account) said they film on an iPhone 12 Pro Max and post without editing. They don't use any compression trick. [V]
- Our source files are mostly 1080×1920 or larger (log.csv: 8 at 1080p, 24 at 1440p–4K, 4 below 1080p), but 0/39 of our posts got a 1080p tier. So low input resolution doesn't explain the gap.
- What's left that we can change is the upload path. We upload through TikTok Studio on the web. elmo and @elsewhere557 most likely post from the phone app, which has the "Upload HD" toggle. That's an inference and hasn't been tested.
- Test (one post): use the p76 setup, but post from the TikTok app (iPad) with Upload HD on and the file exported at 1080×1920. Then check the served tier in the next cloud self pull.
