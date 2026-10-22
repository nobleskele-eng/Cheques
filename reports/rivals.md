# Rival report, run 2026-10-22 (rival-analyst, cloud)
**Coverage** (research/data/*_videos.csv): elsewhere557 578 (newest 10-22 00:05 UTC), someplace505 176 (newest 10-21 19:16). Not tracked: kadzoo55871, anywhere557 (no data files; MASTER names them, no pull script run).
**Pull failure:** someplace505 `pull_tech.py` died with SSL EOF; not retried (rule 4). Its _encoding.csv is the 10-21 copy, so it lacks encoding rows for new posts. elsewhere557 all 3 pulls OK; no 403/captcha.

## Headline changes
- Official track "Let Go" (Ark Patrol) is the live hit sound: elsewhere557 used it 4x in 10-17..10-20 for 5.3M, 826K, 322K, 182K (elsewhere557_videos.csv). It beats MASTER 2.2 ("official tracks lose, 0.36-0.80x").
- Decay continues: weekly median views/post, elsewhere557 102K (wk 09-28) to 20K (wk 10-19, partial); someplace505 19.4K to 11K (partial wk). (videos.csv)
- Last 7 days (since 10-15): elsewhere557 45 posts (6.4/day), median 26.2K; someplace505 27 posts (3.9/day), median 12.2K. 12 elsewhere557 hits (>=1M or >=5x median), 1 someplace505 (117K, own blank-name sound, 6 s).
- elsewhere557 hits: lengths 6-13 s (median 8), fps 24-60 mixed (6 of 12 are 59-60), so no fps signal. Hour (UTC) clusters 00-01 (5 of 12). Opening not checked (no vidIQ used).
- Model (research/success-model.md): AUC unchanged, 0.70 beat-median, 0.69 100K+, 0.51 1M+. Not a forecast for a new account.

## Top 5 sounds to use now (research/data/proven_sounds.csv; xmedian = vs same-week median)
1. oscncs, "original sound", 18.8x, 67% beat, 3 uses, last 10-11. music/x-7692131847752436494
2. Ark Patrol, "Let Go", 11.6x, 83%, 6 uses, last 10-20 (official). music/x-7385586638095321105
3. Cherry, "original sound", 10.4x, 60%, 5 uses, last 10-19. music/x-7632470897454041874
4. yuji, "original sound - yuji", 8.7x, 80%, 5 uses, last 10-01. music/x-7687561451339516693
5. ʚminachiiiɞ, "original sound", 4.5x, 62%, 8 uses, last 10-12. music/x-7600721158866619156
Changes vs 10-21 list: dropped shinobi (1.9x); added "audio originale" by ✧ (4.6x, last 09-01, stale). Let Go and Cherry rose.

## Warnings
- Likely paid promo, skip (proven_sounds.csv): gambling, CIGARETTES, farewell cruel world, i'm tired.
- n is 3-8 per sound; relative views are correlation, and a sound may just ride its clip.
- proven_sounds.py reproduces the old CSV only approximately (70 of 73 sounds matched; view counts drift between pulls). Sound is a lever, not proof.
- Recent-week views are still accruing.

## Suggested MASTER changes
- 2.2: official track "Let Go" 11.6x over 6 uses (proven_sounds.csv); official-vs-account split is not absolute.
- 3 Sound line: swap list to oscncs 18.8x, Let Go 11.6x, Cherry 10.4x, yuji 8.7x, minachii 4.5x.
- 2.10: decay continues (102K to 20K weekly median, elsewhere557).
- New scripts: research/scripts/proven_sounds.py, build_csvs.py.
