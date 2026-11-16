# ANIME: @stayvyxed + @chequethetime current state
Updated 2026-11-16 by local session (v3: Vyx's niche + definitions; 3 tracked editors). Tags: [V] Vyx, [L] local, [C] cloud, [est] estimate. Cap 6,000 bytes. Overwrite, don't append (same rules as MASTER.md).

## 1. Accounts [V 16 Nov unless tagged]
| | @stayvyxed | @chequethetime |
|---|---|---|
| Role | oldest, largest; formal cinematic edits | jugg + "tiktok style" edits: romance and/or thirst traps of popular characters [V 16 Nov] |
| Effort | month(s) per edit, months between posts | hour(s) per edit |
| Goal | keep growing; never get shadowbanned | 1K followers by summer 2027, or drop it |
| Followers [L profile 16 Nov] | 7,499 (1.5M likes) | 91 (4,617 likes); 16 posts, median 872 [vidIQ] |
| Best 2026 | JJK 657K (15 Jan) | Choso 8.8K (14 Feb) |
| Latest | Black Clover 945 (9 Nov) | Ao Haru Ride 434 (16 Nov) |
- **Niche [V 16 Nov]:** "jugg" and "tiktok style" edits, mostly romance and/or thirst traps of popular characters. Both aim to feel sensual, intimate or personal to the viewer.
  - **sasa jugg** (@smokinsasa7, @.sadaqatt): R&B song + soft shakes and blur transitions, focused on a character's look or a relationship (almost always a couple).
  - **tiktok style** (@zrivvn): 1080×1080 edit of one character, slow transitions, soft blur flicker.
- **Audience [V 16 Nov]:** every post over 100K views on either anime account had a majority-female audience, so Vyx plays the shoujo / romance / thirst-trap card hard.
- **Warning on @stayvyxed:** a 300K post was removed ~6 months after posting for "hate speech" (censored n-word in on-screen lyric text). Not appealed. TikTok: strikes expire after 90 days; hitting the limit means 90 days out of For You; deleting a post doesn't remove its strike [web].
- **Posting:** almost all from the phone app; Studio web did no better. Vyx runs scripts that change file metadata to reduce TikTok compression.
- **Credit:** tag the audio/inspiration creator in the caption ("ib/rm @…", "ac @…"). Edits and AE projects stay on D:\, out of git.

## 2. What we know (strongest first)
1. **Average watch time splits hits from flops** [V Studio; seed-cap §5]. Every post at ≥5.9 s got 8.8K–657K views; every post at ≤4.2 s got under 1K (n=9). Most viewers leave at 0:01 even on hits; hits keep more of the rest.
2. **@chequethetime did best with popular characters of an airing show** [vidIQ, all 16 posts]. 12–15 Feb, during JJK S3: 5 edits of that season's side characters (Shoko, Hakari, Choso, Kirara, Megumi) with fan-voice captions ("Hakari is so tuff in the new jjk episode"). Median 4.9K, likes 12.5–19.7%. Sep–Nov: 9 lyric-caption edits across 8 shows, none airing. Median 434, likes 4.8–13.7%.
3. **Hits react:** likes 17.5–20.7%, shares 1.5–2.6%, saves 3.2–5.5%. Black Clover got close on reactions but averaged 4.16 s, so no second batch.
4. **Hits keep earning:** peak on days 2–3, then Search (10–23%) and profile visits (17–31%). Tunnel to Summer and Choso got ~2/3 of their views after day 7 [est]. Flops are ~97% For You and stop within hours.
5. **Search comes from song, show and character names, not hashtags** (JJK: Bryson Tiller queries; Choso: "choso edit PATD" 41%; AOT: "attack on titan edit").
6. **Timing:** both JJK runs (@stayvyxed 657K on 15 Jan, @chequethetime in Feb) landed while JJK S3 aired (from 8 Jan) [web].
7. **Followers per view:** 0.06–0.09% on hits, 0.2–0.27% on small posts. @chequethetime needs ~910 more: ~350K views at Choso's rate [est].
8. **This month** (`research/trends-2026-11-16.md`): the circle runs #loopvember26 (loops mean more rewatches). Airing romance has the most breakouts (Firefly Wedding, Apothecary S3), many from accounts with <3.5K followers. "senju in the new episode 7" (Tokyo Revengers, 81K) shows the episode-reaction format working now.
9. **Reference yields** (`research/character-yield-2026-11-15.md`): romance steady, shonen mostly under 1×.

## 3. Recommendation now
- **Target: average watch ≥6 s** in Studio at 24 h [est, n=9]. Log each post in `anime/log.csv`.
- **Inside the niche** (§1), the Feb data adds: popular characters from a show people are watching now, with a fan-voice caption. Before picking a show, check Vyx's own history with it (AOT: last 3 posts below median [V]).
- **Thirst traps: adult characters only.** Romance edits of teen couples stay sweet, not sensual. TikTok removes content, including animation, that sexualises minors [web], and @stayvyxed already has one violation.
- **Tracked editors:** @smokinsasa7, @.sadaqatt, @zrivvn. `anime/refs.md` lists their posts weekly (Saturday routine).
- **Next @chequethetime edit:** Firefly Wedding (ep 7 Fri 20 Nov), Shinpei × Satoko, a moment from the latest episode, the "my only loooveeee" audio (ac @crvz), fan-voice caption, looped. It also tests romance when it's topical (its romance edits so far weren't on airing shows).
- **First second:** motion or the subject in frame 1. No typed text over black (Ao Haru Ride: 1.96 s).
- **Protect @stayvyxed [proposed]:** no slurs in on-screen text or captions, even censored. Keep the metadata scripts off it until they're tested on @chequethetime.

## 4. Waiting on Vyx
1. **Account status** on @stayvyxed (Settings and privacy → Account → Account status): any active strike?
2. Slur rule: make it a hard rule?
3. Studio screenshots for each new post (`accounts.md` lists them every Saturday).

## 5. How to pull
- **Studio:** Vyx's screenshots → `anime/log.csv`. Studio rows use Vyx's local date; pull rows use UTC.
- **Public lists:** the Saturday routine (from 21 Nov) → `research/data/<handle>_videos.csv` + `accounts.md`. Or vidIQ `vidiq_tiktok_profile_videos` (5 credits a page; **5 left on 16 Nov**, resets 14 Dec). vidIQ can't see frame shape or pace except through its 10-credit watch tool. AniList API is free but needs a User-Agent header.
- **Browser pane:** signed in as @papercheques. Profile headers load; grids and follow lists don't. No scripted pulls. Never hover or play.
