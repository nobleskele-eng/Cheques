# Rival report, run 2026-10-24 (rival-analyst, cloud)
**Coverage** (research/data/*_videos.csv): someplace505 182, elsewhere557 595, anywhere557 174, kadzoo55871 147, .aaapaathy 838, fang_w3 828, rvf5567 4. All 7 pulls OK, no 403/captcha. Note: item_list returned only the newest ~196 for elsewhere557, so older rows were merged back from git HEAD (399 kept).

## Headline changes
- Network still decaying/flat: 7-day median views elsewhere557 23.2K (n44) vs 26.3K prior week; someplace505 20.6K vs 18.7K; .aaapaathy 17.3K vs 34.0K; fang_w3 3.6K vs 6.2K (videos.csv).
- Hits, last 7 days (>=1M or >=5x median): elsewhere557 3.1M (10-21, 7 s, "origineel geluid"), 1.3M "Peace" (8 s), 1.1M "Let Go" (13 s); someplace505 2.2M (10-23 05:16 UTC, 8 s, blank-name sound; 2 more at 186-285K); kadzoo55871 2.0M (10-21, 8 s, "nuts edited"). Lengths 6-13 s, median 8. Opening not checked (no vidIQ).
- kadzoo55871 only 6 posts in 7 d (was 15), median 139K (videos.csv). anywhere557 near-dormant (5 posts, median 8.1K).
- rvf5567: 4 posts, median 370 views, no new post since 10-22 (videos.csv; reports/watch.md). No contradiction with MASTER 2.
- Model (research/success-model.md): AUC 0.70 beat-median, 0.69 100K+, 0.52 1M+. Correlation, not a forecast for a new account.

## Top 5 sounds (proven_sounds.csv; x = vs same-week median)
1. Air, BICEP & SOARR: 31.6x, 67% beat, 3 uses, last 09-18 (stale). music/x-7680603591949715472
2. oscncs, "original sound": 19.2x, 67%, 3 uses, last 10-11. music/x-7692131847752436494
3. yuji, "original sound - yuji": 8.7x, 80%, 5 uses, last 10-01. music/x-7687561451339516693
4. Ark Patrol, "Let Go" (official): 8.1x, 75%, 8 uses, last 10-24. music/x-7385586638095321105
5. zardy, "it be okay by zardy": 7.0x, 100%, 3 uses, last 09-09 (stale). music/x-7662067661410355976
Changes vs 10-22: dropped Cherry; added shinobi. 22 proven of 74 (old list 71 sounds). Let Go fell 11.6x to 8.1x as uses rose 6 to 8.

## Warnings
- Likely paid promo (5 flagged in proven_sounds.csv): skip gambling, CIGARETTES.
- n is 3-8 per sound; ranks 1 and 5 are weeks old and 3 uses only. Sound may ride its clip.
- Recent-week views still accruing; item_list window limits older history.

## Suggested MASTER changes
- 2.2: Let Go now 8.1x over 8 uses (was 11.6x over 6).
- 3 Sound line: oscncs 19.2x, yuji 8.7x, Let Go 8.1x; Cherry dropped.
- 2.9/2.10: weekly median elsewhere557 23.2K, flat vs 26.3K; kadzoo posting slowed to 6/wk.
