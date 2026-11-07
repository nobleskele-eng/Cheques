# Self report, run 2026-11-07 (self-analyst, cloud)
Pull OK: 47 public posts (was 47 on 31 Oct), so no new posts since 30 Oct 01:48 UTC (8 days). Median views 726, median likes/view 5.2%, best 4,645 (10 Oct). Nothing is "still collecting". Counts have crept up slightly (e.g. 30 Oct post 1,005 to 1,067).

| post | UTC | views | like% | share% | save% | s | sound | sched? | tier |
|---|---|---|---|---|---|---|---|---|---|
| p74 | 22 Oct 03:25 | 717 | 2.2 | 0.14 | 0.14 | 8 | Let Go | no | 576p 336k |
| p76 | 23 Oct 00:36 | 742 | 4.0 | 0.00 | 0.27 | 8 | Let Go | no | 576p 617k |
| p77 | 23 Oct 02:51 | 746 | 3.9 | 0.00 | 0.13 | 11 | Let Go | no | 720p 1568k |
| p81 | 24 Oct 02:23 | 807 | 5.2 | 0.50 | 0.25 | 10 | Let Go | no | 576p 505k |
| ? | 24 Oct 22:35 | 737 | 7.6 | 0.27 | 0.14 | 9 | blank-name orig. | no | 576p 950k |
| ? | 25 Oct 23:34 | 793 | 7.9 | 0.13 | 0.38 | 8 | same | no | none |
| ? | 27 Oct 01:51 | 700 | 4.3 | 0.00 | 0.00 | 8 | same | no | none |
| ? | 30 Oct 01:48 | 1,067 | 6.1 | 0.09 | 0.37 | 8 | same | no | none |
(Matches by log.csv time/duration; tiers from papercheques_encoding.csv; sched? = video-ID time vs post time.)

## Recipe test (MASTER section 3)
- Matched p74, p76, p77, p81, n=4: median views 744 (717-807) vs old 712; likes/view 4.0% (2.2-5.2) vs 5.2%; shares 0.07% vs 0.00%. **Too early (n<10).** Direction: views +4% (inside 700 +/- 300 noise), likes slightly lower, shares flat.
- 4 unmapped blank-name-sound posts: median 765 views, likes 7.0% (4.3-7.9). Not scored as recipe posts until mapped. Combined n=8 would still be flat on views (~750) with likes ~5.6%; direction only.
- Milestone (10-15% likes/view): not hit, best 7.9%.
- Ceiling: nothing above 1,067 since 10 Oct. No 1080p tier on any post (0 of the encoding file). No FYP-flag data for these in log.csv; no flag after a lite PASS seen.

## Unmatched, for Vyx
24 Oct 22:35, 25 Oct 23:34, 27 Oct 01:51, 30 Oct 01:48 UTC: which p-numbers, which upload path (app + Upload HD?). No posts for 8 days: is the pipeline (p85-p93) waiting on lite checks?

## Suggested MASTER changes
- Section 1: 47 posts, median 726; no posts since 30 Oct.
- Section 3: recipe n=4 matched, 744 views, 4.0% likes; unchanged verdict, too early.
- Section 5: note the 8-day posting gap; ask what blocks p85-p93.
