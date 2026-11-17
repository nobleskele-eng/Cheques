# ANIME: @stayvyxed + @chequethetime current state
Updated 2026-11-17 by cloud session (v5: Firefly Wedding flop). Tags: [V] Vyx, [L] local, [C] cloud, [est] estimate. Cap 6,000 bytes. Overwrite, don't append.

## 1. Accounts [V 16 Nov unless tagged]
| | @stayvyxed | @chequethetime |
|---|---|---|
| Role | oldest, largest; formal cinematic edits | jugg + "tiktok style" edits: romance and/or thirst traps of popular characters [V 16 Nov] |
| Effort | month(s) per edit, months between posts | hour(s) per edit |
| Goal | keep growing; never get shadowbanned | 1K followers by summer 2027, or drop it |
| Followers [C pull 17 Nov] | 7,495 (1.45M likes) | 90 (4,669 likes); 17 posts, median 886 |
| Best 2026 | JJK 657K (15 Jan) | Choso 8.8K (14 Feb) |
| Latest | Black Clover 945 (9 Nov) | Firefly Wedding 490 (16 Nov) |
- **Niche [V 16 Nov]:** "jugg" and "tiktok style" edits, mostly romance and/or thirst traps of popular characters. Both aim to feel sensual, intimate or personal to the viewer.
  - **sasa jugg** (@smokinsasa7, @.sadaqatt): R&B song + soft shakes and blur transitions, focused on a character's look or a relationship (almost always a couple).
  - **tiktok style** (@zrivvn): 1080×1080 edit of one character, slow transitions, soft blur flicker.
  - **Not these [V 16 Nov]:** *impact* edits (impact frames, strong shakes, harsh rap such as osamason) and *manga animation* (animated manga panels). **Tags can't tell styles apart**: #jugg / #juggedit get used as keyword spam. Only watching can, so Vyx judges style (Claude's 16 Nov picks: 0/3).
- **Audience [V 16 Nov]:** every post over 100K views on either anime account had a majority-female audience, so Vyx plays the shoujo / romance / thirst-trap card hard.
- **Warning on @stayvyxed:** a 300K post was removed ~6 months after posting for "hate speech" (censored n-word in on-screen lyric text). TikTok: strikes expire after 90 days; hitting the limit means 90 days out of For You; deleting a post doesn't remove its strike [web].
- **Posting:** almost all from the phone app (Studio web did no better). Vyx's metadata scripts aim to cut compression.
- **Credit:** tag the audio/inspiration creator in the caption ("ib/rm @…", "ac @…").

## 2. What we know (strongest first)
1. **Average watch time splits hits from flops** [V Studio; seed-cap §5]. Posts at ≥5.9 s got 8.8K–657K views; posts at ≤4.2 s got under 1K (n=10). Most viewers leave at 0:01 even on hits; hits keep more of the rest.
2. **@chequethetime did best with popular characters of an airing show** [vidIQ, all 16 posts]. 12–15 Feb, during JJK S3: 5 edits of that season's side characters (Shoko, Hakari, Choso, Kirara, Megumi) with fan-voice captions ("Hakari is so tuff…"). Median 4.9K, likes 12.5–19.7%. Sep–Nov: 9 lyric-caption edits across 8 shows, none airing. Median 434, likes 4.8–13.7%.
3. **Hits react:** likes 17.5–20.7%, shares 1.5–2.6%, saves 3.2–5.5% (Black Clover matched those but averaged 4.16 s: no second batch).
4. **Hits keep earning:** peak on days 2–3, then Search (10–23%) and profile visits (17–31%). Tunnel to Summer and Choso got ~2/3 of their views after day 7 [est]. Flops are ~97% For You and stop within hours.
5. **Search comes from song, show and character names, not hashtags** (Choso: "choso edit PATD" 41%).
6. **Timing:** both JJK runs (657K on 15 Jan; @chequethetime in Feb) landed while JJK S3 aired [web].
7. **Followers per view:** 0.06–0.09% on hits, 0.2–0.27% on small posts. @chequethetime needs ~910 more: ~350K views at Choso's rate [est].
8. **Our edits flop where the show works [C 17 Nov, n=2]:** Ao Haru Ride 1.96 s, Firefly Wedding 2.5 s (490); both shows broke out on small accounts (`trends-2026-11-16.md`). On-target batch (67% female) gone in ~2 s: it's the opening [est]. Not aspect/quality (hits 4:3 too; Firefly 12.6 Mbps).

## 3. Recommendation now
- **Target: average watch ≥6 s** in Studio at 24 h [est, n=10]. Log each post in `anime/log.csv`.
- **Where show/audio leads come from (16 Nov):** only the tracked editors' results (`refs.md`, weekly) and Vyx's own data. Generic outlier searches mix in other styles. Check Vyx's history with a show first (AOT: last 3 below median [V]). Vyx judges fit.
- **Thirst traps: adult characters only.** Romance edits of teen couples stay sweet, not sensual. TikTok removes content, animation included, that sexualises minors [web]; @stayvyxed already has a violation.
- **Next @chequethetime edit [C 17 Nov]:** Firefly Wedding again, ep 7 footage (Fri 20 Nov), same audio, fan-voice caption; change only the opening (below).
- **First second:** subject in frame 1 isn't enough (Firefly: his bloody face, hers hidden, no text → 2.5 s). Open on both faces, moving, trope line in the empty top bar (like the breakouts). No text over black.
- **No 4K upscaling [16 Nov]:** TikTok caps re-encodes at 1080×1920 (0/748 network videos higher [C]); ~4K original-file posts gave no lift [L]. Export 1080; upscale only crops under 1080 px. After 21 Nov: `research/data/<h>_encoding.csv` vs views.
- **Protect @stayvyxed [proposed]:** no slurs in on-screen text or captions, even censored. Metadata scripts stay off it until tested on @chequethetime.

## 4. Waiting on Vyx
1. **Account status** on @stayvyxed (app: Account → Account status): any active strike?
2. Slur rule: make it a hard rule?
3. Studio screenshots for each new post (`accounts.md` lists them every Saturday).

## 5. How to pull
- **Studio:** Vyx's screenshots → `anime/log.csv`. Studio rows use Vyx's local date; pull rows use UTC.
- **Public lists:** the Saturday routine (from 21 Nov) → `research/data/<handle>_videos.csv` + `accounts.md`. Or vidIQ `vidiq_tiktok_profile_videos` (5 credits a page; **5 left on 16 Nov**, resets 14 Dec). Ask Vyx before spending. AniList API is free but needs a User-Agent header.
- **Browser pane:** signed in as @papercheques. Profile headers load; grids and follow lists don't. No scripted pulls. Never hover or play.
