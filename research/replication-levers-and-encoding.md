# Replication Levers and Encoding (Bitrate) Analysis

**Data:** TikTok's creator video list plus actual video files, pulled 2026-10-21.
**Coverage:** @someplace505 176/176 videos, @elsewhere557 572/581. 22 video files were downloaded, measured with ffprobe and then deleted.
**Related:** [growth regression](tiktok-growth-regression.md) · [content-style analysis](tiktok-someplace505-elsewhere557-analysis.md) · [plain summary](reliability-plain-summary.md)

> **Everything here is correlation, from two accounts that already succeeded.** It shows what went with more views on *these* accounts. It doesn't prove what causes views, and it won't guarantee results on a new account.

---

## 0. Answer: the best evidence-based way to replicate

Ranked by strength of evidence.

**Strong (consistent on both accounts)**
1. **Bake the audio into the video file**, so TikTok labels it "original sound", instead of picking a song from TikTok's library.
   - Same-week relative views: **1.31× and 2.52×** for baked-in audio, vs **0.38× and 0.78×** for library songs used fewer than 5 times. *(Relative views = a video's views ÷ the account's median for that week, so 1.0× is an average week.)*
2. **Upload at full 1080×1920 or above.** @elsewhere557's few uploads without a 1080p tier did **0.21×** (22 videos, only 18% beat their week's median).
3. **Keep daily volume moderate.** Views per post drop beyond ~3 posts/day (@someplace505) and ~6/day (@elsewhere557).
   - On @elsewhere557, days with 2–3 posts did **2.43×** per post, vs **~0.9×** on days with 7+.
   - Its first post of the day did **1.66×**.
   - *Not shown:* whether *total* daily views fall with more posts. More posts are still more chances at a hit.

**Moderate (one account only)**

4. **Original-quality upload: TikTok serves your file without re-encoding it.** On @someplace505 this went with **1.44×** (library song) to **7.23×** (with baked-in audio). See §1.3 for how it appears to be done, and the risk.
5. **Slightly longer clips:** 11–14 s+ did 1.13–1.98× on both accounts, but sample sizes are small.

**No measurable effect (skip)**
- **60 fps vs 30 fps:** @elsewhere557 did 1.00× at ~60 fps vs 1.15× at ~30 fps.
- **Loudness, and TikTok's own quality scores:** correlation with views is ~0, between −0.15 and +0.03.
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

#### Audio

| | @someplace505 | @elsewhere557 |
|---|---|---|
| Baked-in audio ("original sound") | **2.52×** (n=42, 74% beat week median) | **1.31×** (n=278, 56%) |
| Library song used 5+ times | 0.93× (n=67) | 0.88× (n=103) |
| Library song used fewer than 5 times | 0.78× (n=66) | **0.38×** (n=98, 35%) |
| Its own named sound ("original sound - ￴ ￴") | **7.28×** (n=21, 90%) | n/a |
| "lovers rock" (shared by both accounts) | 3.64× (n=21) | 0.85× (n=28) |

#### Upload quality × audio (@someplace505; checks whether the two effects are separate)

| | Baked-in audio | Library song |
|---|---|---|
| Original file served | **7.23×** (n=22, 82%) | 1.44× (n=17, 59%) |
| Re-encoded | 1.18× (n=20, 65%) | 0.84× (n=116, 39%) |

Each factor helps on its own; together they're strongest.

@elsewhere557 has no original-file videos. For it, baked-in audio is 1.31× vs 0.73× for library songs (re-encoded only).

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

## 3. Caveats

1. **Correlation, not cause.** For example, the operator may use the HD upload method or baked-in audio on footage they already think is strongest.
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
