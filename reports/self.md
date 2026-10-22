# Self report, local run 2026-10-22 02:50 UTC (no pull)
[csv] research/data/papercheques_*.csv (39 posts, 21 Oct). [probe] ffprobe. [mtime] export time. Upload = ID>>32. Last-10: git show e1c3fbf.

## 1. Best vs rest [csv]
- The 3 lows are distribution: 31 = scheduled 12 h, 353 (p49) = scheduled 3.5 h, 159 (p67) = 8 min after p64. Scheduled n=3 med 353 vs direct n=36 med 716.
- Hour: the top 4 (2207, 1097, 989, 937) were all posted 23:29-02:20 UTC. See 4.
- TikTok length: no signal (group medians 672-785, 5-11 s).
- Sound: both best = account sounds (1097's also got 458 that night). Proven yuji: 809, best shares 1.36% (n=1).
- Day, posts/day, gap: none. 2207 was the 3rd post in 2h13m.
- Rates: 2207 had 5.3% likes (= median). Top 10 vs bottom 10: likes 6.5% vs 5.1%, any saves 10/10 vs 4/10. Like% falling: 6.3% (3-10 Oct), 5.1% (11-16), 4.2% (18-21).

## 2. Cut short [probe vs csv]
| file | post UTC | file s | TikTok s | basis |
|---|---|---|---|---|
| p5 | 10-04 14:23 | 11.3 | 11 | mtime -3m |
| p10 | 10-05 02:46 | 10.3 | 9 | -3m (p9 same len) |
| p14 car | 10-08 03:05 | 10.3 | 7 | -3m |
| p27 | 10-10 01:42 | 10.0 | 10 | -5m |
| p33 | 10-11 22:34 | 9.6 | 9 | -3m |
| p37 | 10-12 16:02 | 10.0 | 7 | -2m, landscape |
| p36 | 10-12 16:52 | 8.7 | 6 | -2m |
| p39 | 10-12 16:58 | 8.2 | 6 | -1m |
| p48/49/64/67 | log | 8.8/12.5/13.1/18.5 | 6/7/7/9 | link |

**9 of 12 cut** by 1.3-9.5 s (median 3.0 s; 68% kept). All cut posts land at 6-9 s. Since 5 Oct, AE edits and raw Douyin alike. Trim-to-sound-length: not supported (n=2).
Uncertain: 1097 post = p14 train (6.2 s) or p13; p17 = 10-08 03:41 (cut); p18-20 = 10-09 03:15-03:19 (all cut); p21/22 = 10-09 15:05 (kept); p60 = 10-19 01:25 (kept; p59 also 11 s).

## 3. Kept vs cut
Certain n=3 vs 9: med 798 vs 709. With uncertain n=6 vs 13: 755 vs 758, likes 4.8% vs 5.8%. No difference yet; the 2 best were full length.

## 4. Hour [csv]
23:00-02:30 UTC (19:00-22:30 EDT): n=10, med 792, none <650, holds the top 4. 02:30-05:00 UTC: n=19, med 687, 7 of the 8 posts <600, but 6 of 7 were scheduled or stacked. Fits elsewhere557 (5/12 hits 00-01 UTC). 3 of the top 4 were one Friday: day and hour tangled.

## 5. Tonight, ranked
1. Post directly, 40+ min apart, never scheduled (sched n=3; <10 min apart n=4: 758, 912, 461, 159).
2. Before Post, the preview must show the file length (p69 edit 8.6 s, p72 edit 10.9 s). If shorter, stop and note the step (n=12).
3. Day's first post at 19:00-21:00 EDT. It's past that now: max 1 more tonight; best clip tomorrow 19:00 (n=10 vs 19, confounded).

## Unmatched (Vyx to fill in)
- The four 21 Oct posts (IDs ...98946070, ...98956737, ...98967534, ...98967576). The two 04:06 uploads came 15 min after p71/p72 were downloaded: probable, not certain.
- Every post before p48 (no log rows); table 2 = probable files.
log.csv not edited.

## Suggested MASTER changes
- 2.5: cut in 9/12 mapped posts since 5 Oct (median -3.0 s).
- 2.8: scheduled n=3 med 353 vs 716.
- 1: like% falling 6.3% to 4.2%.
