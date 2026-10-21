# Growth Regression: @someplace505 & @elsewhere557

**Data:** pulled directly from TikTok on 2026-10-21 at 19:26 UTC. This is first-party data: each profile's page data plus TikTok's creator video-list endpoint.
**Coverage:**
- @someplace505: 176 of 176 videos.
- @elsewhere557: 572 of 581 videos. The other 9 aren't returned publicly, probably private or under review.

**Integrity check:** summed per-video likes match each profile's total likes, at 99.7% (@someplace505) and 98.3% (@elsewhere557).

**Companion doc:** [content-style analysis](tiktok-someplace505-elsewhere557-analysis.md).

---

## 0. Answer

| | **Scenario 1: 30-day buffer** | **Scenario 2: no buffer** | *Reference: real account creation* |
|---|---|---|---|
| **@someplace505**: start date | 2026-05-17 | 2026-06-16 (first video) | 2026-01-10 |
| Account age at pull | 157.0 days | 127.0 days | 284.6 days |
| Followers / day | **1,364** | **1,686** | 753 |
| Views / day | 682,796 | 844,082 | 376,686 |
| Likes / day | 163,582 | 202,222 | 90,245 |
| Videos / day | 1.12 | 1.39 | 0.62 |
| **@elsewhere557**: start date | 2026-05-30 | 2026-06-29 (first video) | 2024-09-29 |
| Account age at pull | 143.9 days | 113.9 days | 752.0 days |
| Followers / day | **2,642** | **3,339** | 506 |
| Views / day | 2,409,257 | 3,044,039 | 460,933 |
| Likes / day | 582,127 | 735,504 | 111,371 |
| Videos / day | 3.98 | 5.02 | 0.76 |

*Followers / day = actual current followers ÷ age. Views and likes per day = summed lifetime views or likes of all visible videos ÷ age.*

1. **The buffer lowers every average by 19% (@someplace505) and 21% (@elsewhere557).** It adds 30 days to a visible history of only 114–127 days.
2. **Neither scenario describes how these accounts actually grew.** Both sat near-flat for weeks after their first video, then took off suddenly:
   - **@elsewhere557** took off on **2026-08-08**, 40 days after its first video.
   - **@someplace505** took off on **2026-08-31**, 76 days after its first video.

   Averaging growth over the whole age spreads a 3–6-week burst across 4–5 months.
3. **The 30-day buffer is far shorter than reality.** TikTok's own account-creation timestamps put creation **157 days** (@someplace505) and **638 days** (@elsewhere557) before the first visible video. Your scenario 1 instinct (an earlier hidden history) is right; one month is just too short.
4. **Best model: a three-phase piecewise line, R² ≥ 0.99 on every series.** Single curves fit worse: linear R² 0.71 / 0.94, while exponential and power-law fits are poor or negative. Also, **the buffer doesn't change the fitted slope or growth rate at all**. Shifting the start date only moves the intercept, so it only affects averages and power-law curvature (§3).

---

## 1. Current totals (first-party, 2026-10-21)

| | @someplace505 | @elsewhere557 |
|---|---|---|
| Followers | 214,189 | 380,134 |
| Total likes | 25,765,405 | 85,211,852 |
| Videos (profile count / publicly listed) | 176 / 176 | 581 / 572 |
| Following | 3 | 64 |
| Account created | 2026-01-10 | 2024-09-29 |
| Display name last changed | **2026-08-27** | **2026-06-18** |
| First visible video | 2026-06-16 | 2026-06-29 |
| Summed views of visible videos | 107,201,232 | 346,601,053 |
| Median views / video | 20,000 | 97,300 |
| Mean views / video | 609,098 | 605,946 |
| Top 5 videos' share of all views | **43.3%** | 16.9% |
| Biggest video | 20.6M views (2026-10-04) | 17.7M views (2026-10-12) |

**Relaunch signal [inference]:** each account changed its display name shortly before it started growing.
- @elsewhere557 changed its name 11 days before its first visible video.
- @someplace505 changed its name on the same day it posted a now-deleted video, 4 days before takeoff.

That fits an older account being wiped and relaunched, which is your scenario 1 idea, over a much longer hidden period.

---

## 2. Your scenarios: milestone timing (modelled)

TikTok doesn't expose follower history, so followers over time are **modelled as proportional to cumulative likes** (see §7, caveat 2). The dates are the same in every scenario; only the "days from start" changes.

| | Reached 100K followers | Days from start (S1 / S2 / real) | Reached 200K followers | Days from start (S1 / S2 / real) |
|---|---|---|---|---|
| @someplace505 | 2026-09-16 | 121 / 91 / 249 | 2026-10-06 | 141 / 111 / 269 |
| @elsewhere557 | 2026-08-20 | 81 / 51 / 689 | 2026-08-30 | 91 / 61 / 699 |

---

## 3. Curve-fit quality (R² on raw values; 1.0 = perfect)

Each fit runs on daily cumulative totals, from the first visible video to the pull date.

| Series | Linear | Exponential | Power law (S1 / S2 / real) | **Piecewise, 3 phases** |
|---|---|---|---|---|
| @someplace505 videos | 0.683 | 0.794 | 0.350 / −0.054 / 0.628 | **0.999** |
| @someplace505 views | 0.708 | 0.466 | −0.037 / −0.381 / 0.384 | **0.991** |
| @someplace505 likes | 0.709 | 0.305 | −0.103 / −0.411 / 0.342 | **0.991** |
| @elsewhere557 videos | 0.899 | −0.869 | 0.845 / 0.463 / −0.520 | **0.999** |
| @elsewhere557 views | 0.938 | −4.086 | −0.266 / 0.642 / −3.459 | **0.998** |
| @elsewhere557 likes | 0.937 | −4.858 | −0.470 / 0.645 / −4.135 | **0.998** |

**Why linear and exponential show one value:** they come out identical in every scenario. Moving the start date shifts every time value by the same constant, which changes only the intercept, never the slope or growth rate. Only the power law, and the averages in §0, depend on which start you pick.

**Why exponential goes negative for @elsewhere557:** the account accelerated in August and then *decelerated*. An exponential curve can only keep accelerating, so it overshoots badly by October.

---

## 4. What actually happened: the three phases (piecewise fit)

![Cumulative views by post date](img/cumulative_views.svg)

### @elsewhere557

| Series | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|
| Views | until 2026-08-08: **250K/day** | 08-08 → 09-02: **8.22M/day** | after 09-02: **2.64M/day** |
| Likes | until 08-08: 61K/day | 08-08 → 09-02: 1.95M/day | after 09-02: 626K/day |
| Videos posted | until 08-13: 0.5/day | 08-13 → 09-21: 7.5/day | after 09-21: 9.0/day |

**Pattern:** views peaked in a 25-day burst, while posting kept *rising*. Average views per video fell from **2.03M** (week of Aug 10) to **154K** (week of Sep 21) as output went from 34 to 80 videos a week. More volume brought diminishing returns per post. October picked up again: 584K average in the week of Oct 12.

### @someplace505

| Series | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|
| Views | until 2026-08-31: **~0/day** | 08-31 → 10-11: **2.59M/day** | after 10-11: **143K/day** |
| Likes | until 09-06: 5K/day | 09-06 → 09-13: 1.49M/day | after 09-13: 451K/day |
| Videos posted | until 08-30: ~0/day | 08-30 → 09-25: 2.7/day | after 09-25: 4.0/day |

**Pattern:** much more hit-dependent. Five videos produce 43% of all views. The likes curve has a one-week spike (Sep 6–13) driven by 10 videos that each passed 1M views. Phase 3's 143K views/day is **understated**, because the most recent videos are still collecting views (§7, caveat 1).

---

## 5. Weekly breakdown (table view of the chart)

Views and likes are each video's current lifetime totals, grouped by the week it was posted. The last 1–2 weeks are still accruing, and the final week (from Oct 19) is partial.

#### @someplace505

| Week of | Videos posted | Cumulative videos | Views | Likes | Avg views / video | Videos ≥1M views |
|---|---|---|---|---|---|---|
| 2026-06-15 | 1 | 1 | 0.00M | 0.00M | 4.3K | 0 |
| 2026-08-24 | 6 | 7 | 1.01M | 0.24M | 167.7K | 0 |
| 2026-08-31 | 15 | 22 | 7.27M | 1.68M | 485.0K | 2 |
| 2026-09-07 | 16 | 38 | 36.03M | 9.18M | 2,251.8K | 10 |
| 2026-09-14 | 25 | 63 | 17.43M | 3.90M | 697.2K | 5 |
| 2026-09-21 | 18 | 81 | 5.46M | 1.28M | 303.2K | 3 |
| 2026-09-28 | 32 | 113 | 31.21M | 7.42M | 975.5K | 4 |
| 2026-10-05 | 27 | 140 | 5.80M | 1.35M | 214.8K | 2 |
| 2026-10-12 | 28 | 168 | 2.89M | 0.62M | 103.2K | 1 |
| 2026-10-19 | 8 | 176 | 0.09M | 0.02M | 11.8K | 0 |

*(No visible videos were posted between 2026-06-16 and 2026-08-24.)*

#### @elsewhere557

| Week of | Videos posted | Cumulative videos | Views | Likes | Avg views / video | Videos ≥1M views |
|---|---|---|---|---|---|---|
| 2026-06-29 | 1 | 1 | 0.33M | 0.06M | 334.7K | 0 |
| 2026-07-06 | 1 | 2 | 1.20M | 0.23M | 1,200.0K | 1 |
| 2026-07-13 | 1 | 3 | 1.50M | 0.34M | 1,500.0K | 1 |
| 2026-07-20 | 5 | 8 | 3.78M | 0.86M | 755.3K | 1 |
| 2026-07-27 | 2 | 10 | 1.96M | 0.46M | 979.5K | 1 |
| 2026-08-03 | 5 | 15 | 5.16M | 1.27M | 1,031.9K | 1 |
| 2026-08-10 | 34 | 49 | 69.12M | 16.43M | 2,033.0K | 19 |
| 2026-08-17 | 44 | 93 | 54.31M | 12.66M | 1,234.3K | 19 |
| 2026-08-24 | 60 | 153 | 60.94M | 15.25M | 1,015.6K | 20 |
| 2026-08-31 | 61 | 214 | 27.50M | 6.73M | 450.8K | 9 |
| 2026-09-07 | 41 | 255 | 26.90M | 5.34M | 656.1K | 4 |
| 2026-09-14 | 50 | 305 | 14.77M | 2.94M | 295.5K | 6 |
| 2026-09-21 | 80 | 385 | 12.30M | 2.96M | 153.8K | 3 |
| 2026-09-28 | 56 | 441 | 13.83M | 3.26M | 246.9K | 2 |
| 2026-10-05 | 57 | 498 | 16.72M | 3.92M | 293.4K | 3 |
| 2026-10-12 | 55 | 553 | 32.12M | 9.89M | 583.9K | 4 |
| 2026-10-19 | 19 | 572 | 4.16M | 1.15M | 219.1K | 0 |

---

## 6. Engagement ratios (first-party, all visible videos)

| Ratio | @someplace505 | @elsewhere557 |
|---|---|---|
| Likes ÷ views | 23.96% | 24.16% |
| Shares ÷ views | 4.33% | 2.90% |
| Saves ÷ views | 2.66% | 2.48% |
| Comments ÷ views | 0.095% | 0.070% |
| Comments ÷ likes | 0.40% | 0.29% |
| Followers per 1M views | 1,998 | 1,097 |

**Reading:** there's about 1 like for every 4 views (views count plays, not unique people), but almost nobody comments. That fits silent mood clips: there's nothing to reply to. @someplace505 turns views into followers at about 1.8× @elsewhere557's rate.

I don't have a sourced benchmark for these ratios, so I'm not claiming whether they're high or low against TikTok overall.

---

## 7. Caveats

1. **Views are attributed to the day a video was posted.** Each point on the curve is the *current* lifetime views of videos posted up to that day, not what the account's view counter showed then. Videos keep gaining views after posting, so the last ~2 weeks are understated, and phase-3 rates are lower bounds.
2. **Followers over time are modelled, not measured.** TikTok only exposes the current follower count, so the curve assumes followers grew in proportion to likes. The one outside check disagrees: on 2026-08-24 the model says ~165K followers for @elsewhere557, while TokPortal (third-party) reported 106,685. Followers probably lag likes, so treat the milestone dates in §2 as **earliest plausible**.
3. **Survivorship.** The regression only sees videos that still exist.
   - @elsewhere557 hides 9 videos from its public list.
   - TokPortal counted 161 videos on 2026-08-24, but only 102 visible videos are dated on or before that day. If TokPortal is accurate, about 59 videos were deleted since, and deleting underperformers would inflate the surviving averages.
4. **Account creation ≠ start of activity.** The "real creation" column is a measured upper bound on age. What the accounts did before their first visible video (if anything) can't be recovered.
5. **Small number of phases.** The piecewise model is chosen for fit, not theory. Three phases with breakpoints found by grid search isn't a forecast, so **don't extend these lines forward**.

---

## 8. Method and files

- **Profile totals and creation dates:** the page data embedded in `www.tiktok.com/@<handle>` (`userInfo.stats`, `user.createTime`, `user.nickNameModifyTime`).
- **Per-video data:** TikTok's creator video-list endpoint, paged newest to oldest. It gives exact post time, views, likes, comments, shares, saves, duration and sound.
- **Fits:** ordinary least squares in plain Python. The piecewise model is a continuous 3-segment line with both breakpoints chosen by exhaustive search for the lowest error.
- **Files in this repo:**
  - `research/data/someplace505_videos.csv`, `research/data/elsewhere557_videos.csv`: one row per video.
  - `research/img/cumulative_views.svg`: the chart in §4.
  - `research/scripts/`: `pull_items.py` (data pull), `regress.py` (scenarios and single-curve fits), `piecewise.py` (3-phase fit), `chart.py` (chart).
