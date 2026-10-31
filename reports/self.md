# Self report, run 2026-10-31 (self-analyst, cloud)
Pull OK: 47 public posts (research/data/papercheques_videos.csv; was 43 on 24 Oct). Median views all posts 722, median likes/view 5.1%. Of the last 12, one was scheduled (21 Oct 06:00, ~2 h ahead; id-time check), the rest direct. Nothing posted <24 h before this run (latest 30 Oct 01:48 UTC, ~36 h).

| post | UTC | views | like% | share% | save% | s | sound | tier |
|---|---|---|---|---|---|---|---|---|
| p74 | 22 Oct 03:25 | 717 | 2.2 | 0.14 | 0.14 | 8 | Let Go | n/a |
| p76 | 23 Oct 00:36 | 741 | 4.0 | 0.00 | 0.27 | 8 | Let Go | n/a |
| p77 | 23 Oct 02:51 | 745 | 3.9 | 0.00 | 0.13 | 11 | Let Go | n/a |
| p81 | 24 Oct 02:23 | 802 | 5.2 | 0.37 | 0.25 | 10 | Let Go | n/a |
| ? | 24 Oct 22:35 | 735 | 7.6 | 0.27 | 0.14 | 9 | blank-name original | 540p |
| ? | 25 Oct 23:34 | 789 | 8.0 | 0.13 | 0.38 | 8 | same | none |
| ? | 27 Oct 01:51 | 699 | 4.3 | 0.00 | 0.00 | 8 | same | none |
| ? | 30 Oct 01:48 | 1,005 | 6.3 | 0.10 | 0.40 | 8 | same | none |
(p-number matches: p74, p76, p77, p81 by time + log.csv; tiers from papercheques_encoding.csv.)

## Recipe test (MASTER §3)
- **Matched recipe posts (p74, p76, p77, p81), n=4:** median 743 views (range 717-802) vs old baseline 712; likes/view median 4.0% (2.2-5.2) vs 5.2%; shares 0.07% vs 0.00%. **Too early (n<10).** Direction: views +4% (inside the 700 ± 300 noise), likes slightly lower.
- **4 unmatched posts since 24 Oct** (all use the blank-name "original sound", the sound someplace505 uses): median 762 views, likes 6.95% (4.3-8.0%), i.e. the best like rates since the 10 Oct post, and the 30 Oct post (1,005) is the 4th-highest ever. Not scored as recipe posts until Vyx maps them (n=4, could be noise).
- **Milestone (≥10-15% likes/view): not hit.** Best 8.0%.
- Ceiling: no post above ~1,000 views since 10 Oct (best ever 4,565 per this pull; MASTER says 2,207, check). No 1080p tier on any new post (the three latest have no tier data at all). No FYP-flag info in log.csv for these.

## Unmatched, for Vyx
24 Oct 22:35, 25 Oct 23:34, 27 Oct 01:51, 30 Oct 01:48 UTC: which p-numbers (p82? p85-p93)? log.csv has no link for any of them. Was the 30 Oct one posted from the TikTok app with Upload HD (upload-path test)?

## Suggested MASTER changes
- §1: 47 posts, median 722; latest 4 posts like 4.3-8.0%, one at 1,005 views.
- §3 recipe test: n=4 matched, 743 views, 4.0% likes; 4 more unmatched at 6.95%.
- §5: add the 4 unmatched posts; ask which sound/upload path they used.
