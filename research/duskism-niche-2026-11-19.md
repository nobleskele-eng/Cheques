# @duskism niche check: stretched anime ("stretchtok"), 19 Nov 2026
Cloud session, 19 Nov. Data: public creator item_list pulls of 13 accounts (`research/scripts/scout_pull.py`), 729 posts in `research/data/stretchtok_posts_2026-11-19.csv`. Covers only (no video pages, no video files). Lanes hand-coded from covers: `research/img/stretchtok-*.jpg`.

## Answer
**The stretched format works, but only in two lanes: stretched one-character edits with no text (median 13.7K) or stretched clips with relatable text on screen (median 12.1K). Stretched no-text clips mixing shows or scenery sat at a median of 848.**

## What "stretchtok" is (covers + captions, 19 Nov)
- The tag is loose (#stretchtok, #strechtok, #stretched). Its core is **16:9 anime footage stretched to 9:16 with a relatable caption on screen**. Example: @kisukeurahara616 (26.6K followers): `real #animequotes #strechtok #relatableanime`, white centred text over the stretched clip, about 1.3 posts/day.
- The second lane is **stretched with no text, one named character per post**. Example: @qwertyajhg (4.9K followers), 25 May–11 Sep, almost all Naruto. Captions look like `:: #NEJI ー #naruto #anime #fyp #stretched`. Closest to the @duskism plan.
- The tag also catches CapCut "stretch effect" tutorials, gaming clips and square videos. Those aren't this niche.

## Numbers [sourced: item_list pull 19 Nov; views as of the pull]
| Lane | Account | Posts | Median views | Under 1K | 10K+ | 100K+ | Median length |
|---|---|---|---|---|---|---|---|
| Stretched, no text, one named character | @qwertyajhg (9:16 phase) | 45 | 13.7K | 0% | 53% | 13% (one 1.1M) | 15 s |
| Stretched + relatable text | @kisukeurahara616 | 234 | 12.1K | 1% | 58% | 14% (one 4.9M) | 12 s |
| Stretched + relatable text, tiny account | @noxad (68 followers) | 6 | 4.5K | 3 of 6 | 2 of 6 | 1 of 6 (138K) | 18 s |
| Stretched, no text, mixed shows/scenery | @noxad | 12 | 848 | 7 of 12 | 0 of 12 | 0 | 29 s |
| First 10 posts of small accounts, any lane | noxad, yruggl_, sjeiksf, bluddyed | 40 | 1.7K | — | 8 of 40 | 2 of 40 | — |

- Engagement: likes/view 16.3% (@qwertyajhg), 12.2% (@kisukeurahara616). Saves/view 3.2% and 1.4%. For scale, @papercheques runs 5.2% likes/view (MASTER §1).
- Length (@qwertyajhg, n=45): 14 s or less, median 18.4K (n=14); 15–17 s, 16.9K (n=20); 18–20 s, 13.6K (n=7); 21 s+, 6.9K (n=4). Shorter looks better, but the buckets are small [weak].
- Tiny accounts break out: @yruggl_ (154 followers) got 163K on its first post (Gaara, stretched, 9 s). @noxad (68 followers) got 138K on its 7th.
- @qwertyajhg moved to square 576x576 on 24 Sep: median 3.6K (n=11), with bigger spikes (464K, 288K). Too few posts to call.
- Contrast, not stretched: @maybe8later (60.9K followers) posts letterboxed 2000s-anime nostalgia compilations; median 77.7K (n=57). Aesthetic compilations can work without the stretch, but that lane is nostalgia-specific.

## Caveats
- **Survivorship [est]:** every account was found through web search, which surfaces posts that already did well. A random new stretched account will likely land below these medians.
- The noxad text vs no-text split runs into timing: the text posts were Jun–Jul, the no-text posts Sep–Nov.
- Most sounds show as "original sound", so this pull can't name the songs.
- @duskism post 1's frames are on Vyx's PC, not in the repo, so post 1 wasn't compared frame by frame.

## How the pull ran (for next time)
- Logged out on TikTok web from the cloud, hashtag pages show "Something went wrong" (#stretchtok and #animeedit alike), search errors and discover pages redirect to For You. So the hashtag's totals weren't read; accounts came from web search.
- 19 Nov: Vyx's "Hi" environment got 7 TikTok hosts added (page scripts, security SDK, static files, cover images: lf16-tiktok-web, lf16-tiktok-common, lf16-cdn-tos, sf16-sg, mssdk.tiktokw.us, p16/p19-common-sign).
- Re-run: `python3 -I research/scripts/scout_pull.py <outdir> 4 qwertyajhg kisukeurahara616 noxad yruggl_`
