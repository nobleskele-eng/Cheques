# TikTok Study: The Simple Version

This covers @someplace505 and @elsewhere557, using data pulled 2026-10-21. The full detail is in §9 of [tiktok-growth-regression.md](tiktok-growth-regression.md).

---

## 1. Is the data right?

- **Yes.** It came straight from TikTok. Each account's video-by-video numbers add up to its profile totals to within 2%.
- **TikTok rounds big view counts** (for example 20.6M). That could shift totals by about 1%, which doesn't change anything here.
- **One weak spot: followers over time.** TikTok doesn't show follower history, so that line is a guess. A spot check found it off by about half. Don't trust the follower dates.

## 2. Did they grow the same way?

- **Same recipe, and each video has the same odds:**
  - About 1 in 6 videos passes 1 million views on both accounts.
  - An average video gets about 600K views on both.
  - Both get about 1 like for every 4 views.
- **The big difference is how much they post.** @elsewhere557 posted about 3× more videos and got about 3× more views. That explains almost the whole gap.
- **Their timing isn't the same.** Their big weeks came at different, unrelated times.
- **@someplace505 is more hit-or-miss.** Its 5 best videos account for 43% of all its views.

## 3. Could someone copy their path today?

**There's no real number for this.** Getting one would mean tracking lots of copycat accounts from their first day. I won't guess.

Why it's probably hard:
1. **We only studied winners.** The same owner runs at least 3 accounts, and we can't see any that flopped.
2. **Both were old accounts restarted**, not brand-new ones.
3. **It's already wearing off.** @elsewhere557's average views per video fell from about 2 million to about 150K as it posted more.
4. **They sell a "how to make these videos" guide.** That means more copycats competing for the same viewers.

**What can be copied:** the format: an 8-second single shot, no text, a popular sound.
**What can't be copied:** their timing and their lucky hits.

**My call:** low odds of reaching 200K+ followers in about 2 months. That's a judgement, not a measured percentage.

## 4. Can the model predict what happens next?

I tested it by hiding the most recent weeks, predicting them from the earlier data, and checking how far off it was.

| Predicting | How well it did |
|---|---|
| How many videos they'll post | **Decent.** Usually off by 5–30%. |
| Views and likes for @elsewhere557 | **Rough.** Usually off by 10–50%, worst case nearly 100%. |
| Views and likes for @someplace505 | **Basically can't.** Usually off by 60–90%, worst case almost 3× off. |
| Followers | **Can't test it at all.** Don't use it for followers. |

These results are on the generous side: there were only a few test runs, and the model had a little "future" information baked in.

---

## The takeaway

1. The data is solid.
2. Both accounts run the same recipe with the same odds per video.
3. Copying it today is a long shot.
4. The model explains the past, but it can't forecast views or followers.
