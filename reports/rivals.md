# Rival report, run 2026-10-31 (rival-analyst, cloud; weekly re-run 13:00 UTC)
**Coverage** (research/data/*_videos.csv rows): someplace505 208, elsewhere557 624, anywhere557 174, kadzoo55871 151. **FAILED:** the pull stopped at .aaapaathy (pull_music.py SSL EOF; earlier run: `KeyError: 'userInfo'`); .aaapaathy, fang_w3 and rvf5567 NOT refreshed (files are from 27 Oct). Stop rule: not re-run. reports/watch.md has no entry after 27 Oct.

## Headline changes (7 days to 31 Oct 13:00 UTC; recent posts still climbing)
- **someplace505:** 7-day median 19.4K (n28) vs 24.1K prior week; one 2.3M (28 Oct, 8 s, official "hold the line" by drifting.). That sound: 5 uses, 1.74x median, 80% beat, last 30 Oct (proven_sounds.csv; not proven yet). Output up to ~4 posts/day.
- **elsewhere557 down hard:** median 14.9K (n38) vs 119.9K prior week. Best 1.7M (27 Oct, 13 s, original sound), 683K (29 Oct, 9 s).
- **kadzoo55871 restarted but weak:** 4 posts in 7 days, median 22K (prev 180K), best 44.8K "lovers rock". anywhere557: 0 posts in 7 days (last 22 Oct).
- Hits: 8-13 s. Opening not checked (no vidIQ).
- **Model** (research/success-model.md): AUC beat-median 0.66, 100K+ 0.68, 1M+ 0.45 (chance). Correlation only.

## Top 5 sounds (proven_sounds.csv; x = vs same-week median)
1. oscncs "original sound": 13.9x, 67% beat, 3 uses, last 10-11. music/x-7692131847752436494
2. yuji "original sound - yuji": 8.4x, 80%, 5 uses, last 10-01. music/x-7687561451339516693
3. 𝙈𝙃𝘾 "original sound": 6.8x, 100%, 3 uses, last 10-03. music/x-7679868563990383382
4. "original sound - ￴ ￴" (blank): 5.7x, 100%, 4 uses, last 10-05, 3 in Oct (someplace505's own-upload sound). music/x-7691278792282737429
5. Cherry "original sound": 2.3x, 80%, 5 uses, last 10-19.
Stale (not listed): Air 30.8x (last 09-18), zardy 8.8x (09-09), 7dievgssn 6.3x (09-26). **Let Go 8.1x -> 2.1x** (10 uses, 70% beat, last 10-27): fading.

## Warnings
- Likely paid promo (5): gambling, crawling back, CIGARETTES, farewell cruel world, i'm tired.
- n = 3-10 per sound; a sound may just ride its clip. 3 of 7 accounts missing this week.

## Suggested MASTER changes
- 2.2/3 Sound: Let Go 2.1x (10 uses); move to oscncs/yuji.
- 2.9: elsewhere557 median 13.7K (was 117K); kadzoo restarted at 7.7K; someplace505 steady ~20K, one 2.1M.
- 2.10: model AUC 0.66 / 0.68 / 0.45.
- Fix: pull_account.py dies on .aaapaathy; watch routine silent since 27 Oct.
