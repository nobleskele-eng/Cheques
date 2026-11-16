# ANIME: @stayvyxed + @chequethetime current state
Updated 2026-11-16 by local session (v1: Vyx's briefing + 6 Studio screenshots). Tags: [V] Vyx, [L] local, [C] cloud, [est] estimate. Cap 6,000 bytes. Overwrite, don't append (same rules as MASTER.md).

## 1. Accounts [V 16 Nov unless tagged]
| | @stayvyxed | @chequethetime |
|---|---|---|
| Role | oldest, largest; formal cinematic edits | simpler edits: the test lab |
| Effort | month(s) per edit, months between posts | hour(s) per edit |
| Goal | keep growing; never get shadowbanned | 1K followers by summer 2027, or drop it |
| Followers [L profile 16 Nov] | 7,499 (1.5M likes) | 91 (4,617 likes) |
| Best 2026 | JJK 657K (15 Jan) | Choso 8.8K (13 Feb) |
| Latest | Black Clover 945 (9 Nov) | Ao Haru Ride 434 (15 Nov) |
- **Warning on @stayvyxed:** a 300K post was removed ~6 months after posting for "hate speech" because on-screen lyric text had a censored n-word. It wasn't appealed. TikTok: strikes expire after 90 days, hitting the strike limit makes an account For You-ineligible for 90 days, and deleting a post doesn't remove its strike [web].
- **Posting:** almost all from the phone app. Studio web was tried (more hashtags, better quality) and did no better. Vyx runs scripts that change file metadata to reduce TikTok compression.
- **Credit:** tag the audio/inspiration creator in the caption ("ib/rm @…", "ac @…").
- Edits and AE projects stay on D:\, out of git.

## 2. What we know (strongest first)
1. **Average watch time splits hits from flops** [V Studio 16 Nov; seed-cap §5]. Every post at ≥5.9 s got 8.8K–657K views. Every post at ≤4.2 s got under 1K (n=9: 6 anime posts, p98, p99, elmo). Most viewers leave at 0:01 even on hits; hits keep more of the rest.
2. **Hits also react:** likes 17.5–20.7%, shares 1.5–2.6%, saves 3.2–5.5% per view. Black Clover came close (14.5% / 1.7% / 2.4%) but averaged 4.16 s and got no second batch. Ao Haru Ride missed on both (4.8% likes, 0 shares, 1.96 s).
3. **Hits keep earning.** The 3 big hits peaked on days 2–3 [charts]. Search (10–23%) and profile visits (17–31%) kept them going: Tunnel to Summer and Choso got ~2/3 of their views after day 7 [est from charts]. Flops peak within hours. Ao Haru Ride was 97% For You and stopped at ~9 h.
4. **Search comes from song and show names, not hashtags.** JJK: all 5 top queries were Bryson Tiller ("are you listening bryson tiller" 11.8%). Choso: "choso edit PATD" 41%. AOT: "attack on titan edit" 13.3%. Tunnel: "the tunnel to summer" 13%.
5. **Timing:** the JJK hit went up a week after Season 3 premiered (8 Jan 2026) [web]. Tunnel to Summer, a summer film, went up in August [est]. Black Clover was live ("best episode this year") but lost viewers fast, so timing only helps when the edit holds.
6. **Followers per view:** 0.06–0.09% on hits, 0.2–0.27% on small posts. @chequethetime needs ~910 more followers: ~350K views at Choso's rate, or 1–1.5M at hit rates [est].
7. **This month** (`research/trends-2026-11-16.md`, vidIQ): the circle runs #loopvember26 (looped edits, which means more rewatches). Ao Haru Ride works for the refs right now (82.8K in 2 days), so our 434 was the edit, not the show [est]. Small accounts break out: outliers from 276–3.4K-follower accounts, up to 2.5M.
8. **Reference yields** (`research/character-yield-2026-11-15.md`): romance steady (Ao Haru Ride 3.8×), shonen mostly under 1× (JJK 0.66×). Our data disagrees: JJK and AOT are our 2026 hits, and Ao Haru Ride flopped (n=1). The edit and the timing beat a show's average [est].

## 3. Recommendation now
- **Target: average watch ≥6 s** in Studio at 24 h [est threshold, n=9]. Read it with likes, shares, % For You and top searches, and log each post in `anime/log.csv`.
- **Next @chequethetime edit (pick 16 Nov):** AOT, Mikasa → Eren, the "my only loooveeee" audio (ac @crvz), seamless loop of 14–18 s, #loopvember26.
- **@chequethetime = the test lab** (hours per edit): 2–3 edits a week, one big change at a time. Carry what works into @stayvyxed.
- **First second:** motion or the subject in frame 1. No typed text over black (Ao Haru Ride: 1.96 s) [n=1].
- **Pick what people want now:** shows airing or premiering this week, seasonal fits, and songs people search with "edit". Tools: AniList API (to build); Creator Search Insights in the app.
- **Caption = what people search:** show + character + song artist, then the credit.
- **Protect @stayvyxed [proposed, Vyx to confirm]:** no slurs in on-screen text or captions, even censored. Keep the metadata scripts off @stayvyxed until they're tested on @chequethetime. @papercheques' original-file posts got no view lift (MASTER §2.3).

## 4. Waiting on Vyx
1. **Account status** on @stayvyxed (app: Settings and privacy → Account → Account status): any active strike, or "not recommended"?
2. Slur rule: make it a hard rule?
3. Studio screenshots for each new post (`accounts.md` lists them every Saturday).

## 5. How to pull
- **Studio:** Vyx's screenshots (Overview, Traffic source, Search queries) → `anime/log.csv`.
- **Public post lists:** the Saturday routine pulls both accounts (Vyx OK'd 16 Nov; first run 21 Nov) → `research/data/<handle>_videos.csv` + `accounts.md`. Or vidIQ `vidiq_tiktok_profile_videos` (5 credits a page; 65 left on 16 Nov, resets 14 Dec). AniList API is free, but needs a User-Agent header.
- **Browser pane:** it's signed in to a TikTok account, so profile-header reads only. No scripted pulls (an in-page script was blocked 15 Nov). Never hover or play.
